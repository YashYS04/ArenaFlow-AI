from __future__ import annotations

from app.services.routing import find_path, path_distance
from app.services.stadium_data import get_stadium


def test_find_path_basic():
    stadium = get_stadium()
    # Direct edge gate_a -> concourse_lower_sw (40)
    path = find_path(stadium, "gate_a", "concourse_lower_sw")
    assert path is not None
    assert len(path) == 1
    assert path[0].to == "concourse_lower_sw"
    assert path_distance(path) == 40


def test_find_path_same_start_goal():
    stadium = get_stadium()
    path = find_path(stadium, "gate_a", "gate_a")
    assert path == []
    assert path_distance(path) == 0


def test_find_path_invalid_nodes():
    stadium = get_stadium()
    assert find_path(stadium, "gate_invalid", "gate_a") is None
    assert find_path(stadium, "gate_a", "gate_invalid") is None


def test_find_path_step_free_only():
    stadium = get_stadium()
    # concourse_lower_sw -> concourse_upper_w has a non-step-free connection (stairs, distance 50)
    # The step-free route must go via concourse_lower_ne elevator instead:
    # lower_sw -> lower_nw -> lower_ne -> upper_e -> seating_upper -> upper_w (60 + 60 + 55 + 35 + 30 = 240)
    
    standard_path = find_path(stadium, "concourse_lower_sw", "concourse_upper_w", step_free_only=False)
    assert standard_path is not None
    assert path_distance(standard_path) == 50
    assert any(not edge.step_free for edge in standard_path)

    step_free_path = find_path(stadium, "concourse_lower_sw", "concourse_upper_w", step_free_only=True)
    assert step_free_path is not None
    assert path_distance(step_free_path) == 240
    assert all(edge.step_free for edge in step_free_path)


def test_find_path_blocked_zones():
    stadium = get_stadium()
    # Route: concourse_lower_sw -> concourse_lower_se -> concourse_lower_ne (60 + 60 = 120)
    # If concourse_lower_se is blocked, route must go: lower_sw -> lower_nw -> lower_ne (60 + 60 = 120)
    
    path_blocked = find_path(stadium, "concourse_lower_sw", "concourse_lower_ne", blocked_zones={"concourse_lower_se"})
    assert path_blocked is not None
    assert path_distance(path_blocked) == 120
    assert "concourse_lower_se" not in [edge.to for edge in path_blocked]

    # To make it unreachable, we must block all exit edges from concourse_lower_sw:
    # lower_se, lower_nw, seating_lower, upper_w
    path_unreachable = find_path(
        stadium, 
        "concourse_lower_sw", 
        "concourse_lower_ne", 
        blocked_zones={"concourse_lower_se", "concourse_lower_nw", "concourse_upper_w", "seating_lower"}
    )
    assert path_unreachable is None


def test_find_path_start_or_goal_blocked():
    stadium = get_stadium()
    assert find_path(stadium, "gate_a", "gate_b", blocked_zones={"gate_a"}) is None
    assert find_path(stadium, "gate_a", "gate_b", blocked_zones={"gate_b"}) is None


def test_find_path_crowd_congestion_weighting():
    stadium = get_stadium()
    # Route: concourse_lower_sw -> concourse_lower_se (distance 60)
    # vs alternative route: lower_sw -> lower_nw -> lower_ne -> lower_se (60 + 60 + 60 = 180)
    # If lower_se is 'high' crowd, its path cost multiplier is 3.0.
    
    crowd_levels = {"concourse_lower_se": "high"}
    path = find_path(stadium, "concourse_lower_sw", "concourse_lower_ne", crowd_levels=crowd_levels)
    assert path is not None
    assert [edge.to for edge in path] == ["concourse_lower_nw", "concourse_lower_ne"]
