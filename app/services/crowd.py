from __future__ import annotations

from app.services.stadium_data import Stadium

_LEVELS = ("low", "medium", "high")
_LEVEL_INDEX = {level: i for i, level in enumerate(_LEVELS)}


def _clamp(index: int) -> str:
    return _LEVELS[max(0, min(len(_LEVELS) - 1, index))]


def effective_crowd(stadium: Stadium, zone_id: str, minutes_to_kickoff: int | None) -> str:
    """Return the simulated crowd level (low / medium / high) for a zone.

    Rules (only applied to surge zone types, e.g. gates & concourses):
      * imminent window (0..10 min before kickoff): +2 levels
      * pre-match window (10..30 min before kickoff): +1 level
      * match underway (minutes < 0): gates relax by 1 level
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
    """Calculate and return effective crowd levels for all zones in the stadium."""
    return {
        zone_id: effective_crowd(stadium, zone_id, minutes_to_kickoff)
        for zone_id in stadium.zone_ids()
    }
