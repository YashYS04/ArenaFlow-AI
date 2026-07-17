from __future__ import annotations

import uuid
from dataclasses import dataclass


@dataclass
class Incident:
    id: str
    zone_id: str
    issue_type: str  # "spill" | "congestion" | "maintenance" | "medical"
    description: str
    resolved: bool = False


class IncidentManager:
    def __init__(self) -> None:
        self._incidents: dict[str, Incident] = {}

    def report_incident(self, zone_id: str, issue_type: str, description: str) -> Incident:
        inc_id = f"inc_{uuid.uuid4().hex[:8]}"
        incident = Incident(
            id=inc_id,
            zone_id=zone_id,
            issue_type=issue_type,
            description=description,
        )
        self._incidents[inc_id] = incident
        return incident

    def get_active_blocked_zones(self) -> set[str]:
        # Block zones with active spills, medical emergencies, or maintenance issues.
        # "congestion" slows down routing (increases crowd cost) but doesn't block it entirely.
        return {
            inc.zone_id
            for inc in self._incidents.values()
            if not inc.resolved and inc.issue_type in {"spill", "maintenance", "medical"}
        }

    def get_all_incidents(self) -> list[Incident]:
        return list(self._incidents.values())

    def resolve_incident(self, incident_id: str) -> bool:
        if incident_id in self._incidents:
            self._incidents[incident_id].resolved = True
            return True
        return False

    def reset(self) -> None:
        self._incidents.clear()


# Process-wide singleton
_manager = IncidentManager()


def get_incident_manager() -> IncidentManager:
    return _manager
