from __future__ import annotations

from dataclasses import dataclass

from app.models.schemas import (
    AccessibilityMode,
    AccessibilityNeed,
    AssistResponse,
    CrowdLevel,
    DestinationIntent,
    FacilityInfo,
    Persona,
    RouteStep,
    UserContext,
)
from app.services import phrasing
from app.services.crowd import effective_crowd, get_all_crowd_levels
from app.services.incidents import get_incident_manager
from app.services.llm import LLMClient
from app.services.phrasing import PhrasingContext
from app.services.routing import find_path, path_distance
from app.services.stadium_data import Edge, Facility, Stadium, localized

_INTENT_TO_TYPES: dict[DestinationIntent, set[str]] = {
    DestinationIntent.restroom: {"restroom", "accessible_restroom"},
    DestinationIntent.first_aid: {"first_aid"},
    DestinationIntent.concession: {"concession"},
    DestinationIntent.guest_services: {"guest_services"},
    DestinationIntent.water: {"water"},
    DestinationIntent.sensory_room: {"sensory_room"},
    DestinationIntent.exit: {"exit"},
    DestinationIntent.gate: {"gate"},
}

_SWAP_ELIGIBLE = {
    DestinationIntent.restroom,
    DestinationIntent.concession,
    DestinationIntent.water,
    DestinationIntent.guest_services,
    DestinationIntent.sensory_room,
    DestinationIntent.gate,
    DestinationIntent.exit,
}

_CROWD_INDEX = {CrowdLevel.low: 0, CrowdLevel.medium: 1, CrowdLevel.high: 2}
_HURRY_INTENTS = {DestinationIntent.gate, DestinationIntent.seat}


class RouteNotFound(Exception):
    """Exception raised when no path can be computed between stadium zones.

    This usually happens due to step-free requirements isolating zones,
    or active spill/maintenance incidents blocking concourse connections.
    """
    pass


@dataclass
class DecisionResult:
    """Carries the outputs of the deterministic rules engine.

    Attributes:
        facility: The chosen facility destination.
        route_steps: Ordered list of path edge instructions.
        crowd_level: Crowd congestion index at destination.
        language: ISO code of resolved output language.
        accessibility_mode: Screen reader, captioned, or standard mode.
        landmark_based: True if directions should utilize landmark text references.
        hurry: True if match kickoff is imminent and speed is prioritized.
        alternatives_note: Optional warning warning if destination was swapped due to crowd.
        urgency: Localized urgency alert text if kickoff is close.
        incident_id: Tracking ID of any logged incident.
        incident_type: Category of any logged incident.
        incident_desc: Description of any logged incident.
    """
    facility: FacilityInfo
    route_steps: list[RouteStep]
    crowd_level: CrowdLevel
    language: str
    accessibility_mode: AccessibilityMode
    landmark_based: bool
    hurry: bool
    alternatives_note: str | None
    urgency: str | None
    incident_id: str | None = None
    incident_type: str | None = None
    incident_desc: str | None = None


def _to_facility_info(facility: Facility, language: str) -> FacilityInfo:
    """Format database Facility record into schema FacilityInfo with localization.

    Args:
        facility: Database facility instance.
        language: Target language code.

    Returns:
        FacilityInfo: Structured API response model.
    """
    return FacilityInfo(
        id=facility.id,
        name=localized(facility.names, language) or facility.id,
        type=facility.type,
        zone=facility.zone,
        accessible=facility.accessible,
        landmark=localized(facility.landmarks, language),
    )


def _resolve_seat(ctx: UserContext, stadium: Stadium) -> Facility:
    """Locate the target seating zone facility based on the ticket section code.

    Args:
        ctx: Current user query context.
        stadium: The stadium database instance.

    Returns:
        Facility: The resolved seating zone facility.
    """
    section = (ctx.ticket_section or "").strip()
    upper = bool(section) and section[0] in {"2", "3", "4"}
    target_id = "seat_upper" if upper else "seat_lower"
    for facility in stadium.facilities:
        if facility.id == target_id:
            return facility
    raise RouteNotFound("Seat facility fixture missing.")  # pragma: no cover


def _candidates_with_routes(
    ctx: UserContext,
    stadium: Stadium,
    types: set[str],
    *,
    accessible_only: bool,
    step_free: bool,
    blocked_zones: set[str],
    crowd_levels: dict[str, str],
) -> list[tuple[Facility, list[Edge], int]]:
    """Scan facilities matching target types and check if there's a valid path.

    Filters candidates by accessibility and returns them sorted by distance.

    Args:
        ctx: User query context.
        stadium: Stadium database.
        types: Set of target facility categories to scan.
        accessible_only: True if only wheelchair-accessible targets should be scanned.
        step_free: True if Dijkstra should restrict path edges to step-free.
        blocked_zones: Active hazard zones to avoid.
        crowd_levels: Crowd multiplier values.

    Returns:
        list[tuple[Facility, list[Edge], int]]: List of tuples of (facility, path, distance).
    """
    results: list[tuple[Facility, list[Edge], int]] = []
    for facility in stadium.facilities_of_types(types, accessible_only=accessible_only):
        path = find_path(
            stadium,
            ctx.current_location,
            facility.zone,
            step_free_only=step_free,
            blocked_zones=blocked_zones,
            crowd_levels=crowd_levels,
        )
        if path is None:
            continue
        results.append((facility, path, path_distance(path)))

    results.sort(key=lambda item: (item[2], item[0].id))
    return results


def _build_route_steps(
    stadium: Stadium, start: str, path: list[Edge], facility: Facility, language: str
) -> list[RouteStep]:
    """Compile a list of edge objects into structured, localized RouteStep models.

    Args:
        stadium: Stadium database.
        start: Starting zone ID.
        path: Dijkstra edges output.
        facility: The target facility.
        language: Language code.

    Returns:
        list[RouteStep]: Sequential route navigation steps.
    """
    steps: list[RouteStep] = []
    facility_name = localized(facility.names, language) or facility.id
    node = start
    for i, edge in enumerate(path):
        is_final = i == len(path) - 1
        landmark = localized(facility.landmarks, language) if is_final else None
        steps.append(
            RouteStep(
                order=i + 1,
                from_zone=node,
                to_zone=edge.to,
                means=edge.means,
                step_free=edge.step_free,
                distance=edge.distance,
                landmark=landmark,
                instruction=phrasing.step_instruction(
                    edge.means,
                    stadium.zone_name(edge.to, language),
                    landmark,
                    is_final=is_final,
                    facility_name=facility_name,
                    language=language,
                ),
            )
        )
        node = edge.to
    return steps


def build_decision(ctx: UserContext, stadium: Stadium) -> DecisionResult:
    """Execute the deterministic rules engine to resolve navigation goals and paths.

    Calculates accessibility constraints, evaluates time-based crowd congestion,
    applies hazard blocks, logs staff incidents, and swaps overcrowded amenities.

    Args:
        ctx: The validated UserContext payload.
        stadium: The stadium layout database.

    Returns:
        DecisionResult: Fully resolved navigation goals, paths, and metadata.
    """
    needs = set(ctx.accessibility_needs)
    wheelchair = AccessibilityNeed.wheelchair in needs
    visual = AccessibilityNeed.visual in needs
    hearing = AccessibilityNeed.hearing in needs

    accessible_only = wheelchair or visual
    step_free = wheelchair or visual

    if visual:
        mode = AccessibilityMode.screen_reader
    elif hearing:
        mode = AccessibilityMode.captioned
    else:
        mode = AccessibilityMode.standard

    # Load active incident blocks and time-based crowd levels
    incident_manager = get_incident_manager()
    blocked_zones = incident_manager.get_active_blocked_zones()
    crowd_levels = get_all_crowd_levels(stadium, ctx.minutes_to_kickoff)

    incident_id: str | None = None
    if ctx.persona == Persona.staff and ctx.incident_report:
        # Staff Persona: Log reported incidents
        issue_type = ctx.reported_issue_type or "maintenance"
        incident = incident_manager.report_incident(
            zone_id=ctx.current_location,
            issue_type=issue_type,
            description=ctx.incident_report,
        )
        incident_id = incident.id
        # Update blocked zones since a new incident was added
        blocked_zones = incident_manager.get_active_blocked_zones()

    # Resolve target facility + route
    if ctx.destination_intent == DestinationIntent.seat:
        facility = _resolve_seat(ctx, stadium)
        path = find_path(
            stadium,
            ctx.current_location,
            facility.zone,
            step_free_only=step_free,
            blocked_zones=blocked_zones,
            crowd_levels=crowd_levels,
        )
        if path is None:
            raise RouteNotFound("No accessible route to seat under current constraints.")
        alternatives_note: str | None = None
    else:
        types = _INTENT_TO_TYPES[ctx.destination_intent]
        candidates = _candidates_with_routes(
            ctx,
            stadium,
            types,
            accessible_only=accessible_only,
            step_free=step_free,
            blocked_zones=blocked_zones,
            crowd_levels=crowd_levels,
        )
        if not candidates:
            raise RouteNotFound(
                f"No reachable facility for intent {ctx.destination_intent.value}."
            )
        facility, path, _dist = candidates[0]
        facility, path, alternatives_note = _maybe_swap_for_crowd(
            ctx, stadium, facility, path, candidates, blocked_zones, crowd_levels
        )

    crowd_level = CrowdLevel(effective_crowd(stadium, facility.zone, ctx.minutes_to_kickoff))
    hurry = ctx.minutes_to_kickoff < 15 and ctx.destination_intent in _HURRY_INTENTS
    urgency = phrasing.urgency_note(ctx.language.value) if hurry else None

    route_steps = _build_route_steps(
        stadium, ctx.current_location, path, facility, ctx.language.value
    )

    return DecisionResult(
        facility=_to_facility_info(facility, ctx.language.value),
        route_steps=route_steps,
        crowd_level=crowd_level,
        language=ctx.language.value,
        accessibility_mode=mode,
        landmark_based=visual,
        hurry=hurry,
        alternatives_note=alternatives_note,
        urgency=urgency,
        incident_id=incident_id,
        incident_type=ctx.reported_issue_type,
        incident_desc=ctx.incident_report,
    )


def _maybe_swap_for_crowd(
    ctx: UserContext,
    stadium: Stadium,
    facility: Facility,
    path: list[Edge],
    candidates: list[tuple[Facility, list[Edge], int]],
    blocked_zones: set[str],
    crowd_levels: dict[str, str],
) -> tuple[Facility, list[Edge], str | None]:
    """Check if the closest facility is highly crowded and swap to a quieter nearby alternative.

    Args:
        ctx: User context query.
        stadium: Stadium database.
        facility: The initially selected closest facility.
        path: Path to the initially selected facility.
        candidates: List of other valid candidate facilities.
        blocked_zones: Active blocked zones.
        crowd_levels: Current crowd levels.

    Returns:
        tuple[Facility, list[Edge], Optional[str]]: Swapped facility, route path, and warning note.
    """
    if ctx.destination_intent not in _SWAP_ELIGIBLE:
        return facility, path, None

    primary_crowd = CrowdLevel(effective_crowd(stadium, facility.zone, ctx.minutes_to_kickoff))
    if primary_crowd != CrowdLevel.high:
        return facility, path, None

    alternatives: list[tuple[int, int, str, Facility, list[Edge]]] = []
    for cand, cand_path, cand_dist in candidates:
        if cand.id == facility.id:
            continue
        cand_crowd = CrowdLevel(effective_crowd(stadium, cand.zone, ctx.minutes_to_kickoff))
        if cand_crowd == CrowdLevel.high:
            continue
        alternatives.append((_CROWD_INDEX[cand_crowd], cand_dist, cand.id, cand, cand_path))

    if not alternatives:
        return facility, path, None

    alternatives.sort(key=lambda a: (a[0], a[1], a[2]))
    _, _, _, alt_facility, alt_path = alternatives[0]
    note = phrasing.alternatives_note(alt_facility.type, ctx.language.value)
    return alt_facility, alt_path, note


async def run_assist(ctx: UserContext, stadium: Stadium, llm: LLMClient) -> AssistResponse:
    """Orchestrate the smart assistant pipeline.

    1. Resolves Dijkstra routing & operational stats using build_decision.
    2. Builds the PhrasingContext data block.
    3. Triggers the Gemini LLM if a free-text question is present,
       otherwise short-circuits instantly to the offline template generator.

    Args:
        ctx: The validated UserContext.
        stadium: The stadium layout database.
        llm: The configured Gemini LLM client.

    Returns:
        AssistResponse: Structured API response model containing routing and phrasing text.
    """
    decision = build_decision(ctx, stadium)

    phrasing_ctx = PhrasingContext(
        language=decision.language,
        facility_name=decision.facility.name,
        facility_type=decision.facility.type,
        facility_landmark=decision.facility.landmark,
        crowd_level=decision.crowd_level.value,
        accessibility_mode=decision.accessibility_mode.value,
        landmark_based=decision.landmark_based,
        hurry=decision.hurry,
        alternative_type=decision.facility.type if decision.alternatives_note else None,
        total_distance=sum(step.distance for step in decision.route_steps),
        step_count=len(decision.route_steps),
        persona=ctx.persona.value,
        incident_id=decision.incident_id,
        incident_type=decision.incident_type,
        incident_desc=decision.incident_desc,
    )

    if ctx.question:
        answer = await llm.phrase(phrasing_ctx, ctx.question)
        used_llm = llm.is_live
    else:
        answer = phrasing.render_answer(phrasing_ctx)
        used_llm = False

    return AssistResponse(
        answer=answer,
        route_steps=decision.route_steps,
        facility=decision.facility,
        crowd_level=decision.crowd_level,
        language=ctx.language,
        accessibility_mode=decision.accessibility_mode,
        alternatives_note=decision.alternatives_note,
        urgency=decision.urgency,
        used_llm=used_llm,
        incident_action_logged=decision.incident_id,
    )
