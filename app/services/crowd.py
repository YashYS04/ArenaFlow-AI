from __future__ import annotations

from app.services.stadium_data import Stadium

_LEVELS = ("low", "medium", "high")
_LEVEL_INDEX = {level: i for i, level in enumerate(_LEVELS)}


def _clamp(index: int) -> str:
    """Clamp index to valid crowd level indices and return the level label.

    Args:
        index: The computed index of the crowd level.

    Returns:
        str: "low", "medium", or "high".
    """
    return _LEVELS[max(0, min(len(_LEVELS) - 1, index))]


def effective_crowd(stadium: Stadium, zone_id: str, minutes_to_kickoff: int | None) -> str:
    """Simulate and return the time-dependent crowd level for a stadium zone.

    Rules for surge zone types (gates and concourses):
      * 0 to 10 minutes before kickoff (imminent window): +2 levels.
      * 10 to 30 minutes before kickoff (pre-match window): +1 level.
      * After kickoff (minutes_to_kickoff < 0): gates relax by -1 level due to inward flow easing.

    Args:
        stadium: The stadium layout database.
        zone_id: The zone identifier.
        minutes_to_kickoff: Minutes remaining until the match starts.

    Returns:
        str: The effective crowd level ("low", "medium", or "high").
    """
    base_index = _LEVEL_INDEX.get(stadium.base_crowd(zone_id), 0)
    if minutes_to_kickoff is None:
        return _clamp(base_index)

    sim = stadium.crowd_sim
    surge_types = set(sim.get("surge_zone_types", []))
    zone_type = stadium.zone_type(zone_id)
    bump = 0

    if zone_type in surge_types:
        pre = int(sim.get("pre_match_window_minutes", 30))
        imminent = int(sim.get("imminent_window_minutes", 10))
        if 0 <= minutes_to_kickoff <= imminent:
            bump += 2
        elif imminent < minutes_to_kickoff <= pre:
            bump += 1

    if minutes_to_kickoff < 0 and zone_type == "gate" and sim.get("in_play_gate_relief"):
        bump -= 1

    return _clamp(base_index + bump)


def get_all_crowd_levels(stadium: Stadium, minutes_to_kickoff: int | None) -> dict[str, str]:
    """Calculate and return effective crowd levels for all stadium zones.

    Args:
        stadium: The stadium layout database.
        minutes_to_kickoff: Minutes remaining until kickoff.

    Returns:
        dict[str, str]: Map of zone IDs to their calculated effective crowd levels.
    """
    return {
        zone_id: effective_crowd(stadium, zone_id, minutes_to_kickoff)
        for zone_id in stadium.zone_ids()
    }
