from __future__ import annotations

import heapq
from app.services.stadium_data import Edge, Stadium


def find_path(
    stadium: Stadium,
    start: str,
    goal: str,
    *,
    step_free_only: bool = False,
    blocked_zones: set[str] | None = None,
    crowd_levels: dict[str, str] | None = None,
) -> list[Edge] | None:
    """Return the list of edges from start to goal.

    Returns an empty list when start == goal, and None when no route
    exists under the given constraints.
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
            weight_multiplier = 1.0
            if crowd_levels:
                crowd = crowd_levels.get(edge.to, "low")
                if crowd == "medium":
                    weight_multiplier = 1.5
                elif crowd == "high":
                    weight_multiplier = 3.0

            edge_cost = int(edge.distance * weight_multiplier)
            new_cost = cost + edge_cost

            if new_cost < best_cost.get(edge.to, float("inf")):
                best_cost[edge.to] = new_cost
                came_from[edge.to] = (node, edge)
                heapq.heappush(frontier, (new_cost, edge.to))

    return None


def _reconstruct(came_from: dict[str, tuple[str, Edge]], goal: str) -> list[Edge]:
    path: list[Edge] = []
    node = goal
    while node in came_from:
        prev, edge = came_from[node]
        path.append(edge)
        node = prev
    path.reverse()
    return path


def path_distance(path: list[Edge]) -> int:
    return sum(edge.distance for edge in path)
