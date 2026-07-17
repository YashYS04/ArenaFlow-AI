from __future__ import annotations

from app.services.crowd import effective_crowd, get_all_crowd_levels
from app.services.stadium_data import get_stadium


def test_effective_crowd_no_kickoff_time():
    stadium = get_stadium()
    # Should fall back to base crowd level in crowd.json
    assert effective_crowd(stadium, "gate_c", None) == "low"
    assert effective_crowd(stadium, "concourse_lower_sw", None) == "high"


def test_effective_crowd_pre_match_surge():
    stadium = get_stadium()
    # 20 minutes to kickoff: pre-match window -> +1 level
    # gate_c base = low -> medium
    assert effective_crowd(stadium, "gate_c", 20) == "medium"
    # concourse_lower_sw base = high -> clamps to high
    assert effective_crowd(stadium, "concourse_lower_sw", 20) == "high"


def test_effective_crowd_imminent_surge():
    stadium = get_stadium()
    # 5 minutes to kickoff: imminent window -> +2 levels
    # gate_c base = low -> high
    assert effective_crowd(stadium, "gate_c", 5) == "high"


def test_effective_crowd_match_underway_gate_relief():
    stadium = get_stadium()
    # -10 minutes (match in progress): gates relax by 1 level
    # gate_a base = medium -> low
    assert effective_crowd(stadium, "gate_a", -10) == "low"


def test_get_all_crowd_levels():
    stadium = get_stadium()
    levels = get_all_crowd_levels(stadium, 20)
    assert len(levels) == len(stadium.zone_ids())
    assert levels["gate_c"] == "medium"
