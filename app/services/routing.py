from __future__ import annotations

import heapq

from app.services.stadium_data import Edge, Stadium


def _get_weight_multiplier(zone: str, crowd_levels: dict[str, str] | None) -> float:
    """Calculate the dynamic edge cost weight multiplier based on the zone's crowd level.

    Args:
        zone: The target zone ID.
        crowd_levels: Map of zone IDs to their active crowd levels ("low"/"medium"/"high").

    Returns:
        float: Multiplier (1.0 for low/none, 1.5 for medium, 3.0 for high).
    """
    if not crowd_levels:
        return 1.0
    crowd = crowd_levels.get(zone, "low")
    if crowd == "medium":
        return 1.5
    if crowd == "high":
        return 3.0
    return 1.0


def find_path(
    stadium: Stadium,
    start: str,
    goal: str,
    *,
    step_free_only: bool = False,
    blocked_zones: set[str] | None = None,
    crowd_levels: dict[str, str] | None = None,
) -> list[Edge] | None:
    """Compute the shortest path between start and goal zones using Dijkstra's algorithm.

    This pathfinder filters traversal based on step-free requirements and avoids
    blocked hazard zones. Node traversal costs are dynamically scaled by crowd congestion.

    Args:
        stadium: The stadium layout database.
        start: The starting zone ID.
        goal: The destination zone ID.
        step_free_only: If True, restricts traversal to ramps, elevators, and walkways.
        blocked_zones: Set of zone IDs that are blocked due to hazards/spills.
        crowd_levels: Active crowd level map for dynamic weight adjustments.

    Returns:
        Optional[list[Edge]]: List of edges forming the shortest path, or None if unreachable.
    """
    if start == goal:
        return []
    if start not in stadium.zones or goal not in stadium.zones:
        return None

    # Priority queue of (cumulative_cost, zone_id).
    frontier: list[tuple[int, str]] = [(0, start)]
    best_cost: dict[str, int] = {start: 0}
    came_from: dict[str, tuple[str, Edge]] = {}

    blocked = blocked_zones or set()

    # If the start or goal itself is blocked, we can't route.
    if start in blocked or goal in blocked:
        return None

    while frontier:
        cost, node = heapq.heappop(frontier)
        if node == goal:
            return _reconstruct(came_from, goal)
        if cost > best_cost.get(node, float("inf")):
            continue

        for edge in stadium.neighbors(node):
            # Check step-free constraints
            if step_free_only and not edge.step_free:
                continue

            # Check if destination zone is blocked by an incident
            if edge.to in blocked:
                continue

            # Calculate dynamic weight multiplier based on crowd level
            weight_multiplier = _get_weight_multiplier(edge.to, crowd_levels)

            edge_cost = int(edge.distance * weight_multiplier)
            new_cost = cost + edge_cost

            if new_cost < best_cost.get(edge.to, float("inf")):
                best_cost[edge.to] = new_cost
                came_from[edge.to] = (node, edge)
                heapq.heappush(frontier, (new_cost, edge.to))

    return None


def _reconstruct(came_from: dict[str, tuple[str, Edge]], goal: str) -> list[Edge]:
    """Rebuild the sequence of edges traversed from start to goal.

    Args:
        came_from: Map of node ID to its predecessor node ID and traversed edge.
        goal: Target destination zone ID.

    Returns:
        list[Edge]: Sequential list of edges from start to goal.
    """
    path: list[Edge] = []
    node = goal
    while node in came_from:
        prev, edge = came_from[node]
        path.append(edge)
        node = prev
    path.reverse()
    return path


def path_distance(path: list[Edge]) -> int:
    """Sum up the total traversal distance for a given path sequence.

    Args:
        path: A sequence of edges representing the route.

    Returns:
        int: Cumulative distance in meters.
    """
    return sum(edge.distance for edge in path)
