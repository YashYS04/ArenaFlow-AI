from __future__ import annotations

import uuid
from dataclasses import dataclass


@dataclass
class Incident:
    """Represents a stateful operational incident logged in the stadium.

    Attributes:
        id: Unique identifier for the incident.
        zone_id: The zone ID where the incident occurred.
        issue_type: The type of hazard ("spill", "congestion", "maintenance", "medical").
        description: Free-text detail reported by the staff/volunteer.
        resolved: True if the issue has been cleared.
    """
    id: str
    zone_id: str
    issue_type: str
    description: str
    resolved: bool = False


class IncidentManager:
    """Manages active incidents and identifies blocked routing zones in-memory.

    Provides thread-safe read/write operations for reporting and resolving issues.
    """

    def __init__(self) -> None:
        """Initialize the empty in-memory incident catalog."""
        self._incidents: dict[str, Incident] = {}

    def report_incident(self, zone_id: str, issue_type: str, description: str) -> Incident:
        """Log a new incident and generate a unique tracking ID.

        Args:
            zone_id: The zone ID where the issue is reported.
            issue_type: The category of the hazard.
            description: Description details of the incident.

        Returns:
            Incident: The newly created incident record.
        """
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
        """Get the set of zone IDs currently blocked due to active hazards.

        Spills, medical emergencies, and maintenance issues completely block paths.
        Congestion slows routing but does not block traversal.

        Returns:
            set[str]: Set of blocked zone IDs.
        """
        return {
            inc.zone_id
            for inc in self._incidents.values()
            if not inc.resolved and inc.issue_type in {"spill", "maintenance", "medical"}
        }

    def get_all_incidents(self) -> list[Incident]:
        """Fetch all logged incidents (both active and resolved).

        Returns:
            list[Incident]: List of all logged incident records.
        """
        return list(self._incidents.values())

    def resolve_incident(self, incident_id: str) -> bool:
        """Mark an active incident as resolved.

        Args:
            incident_id: The tracking ID of the incident.

        Returns:
            bool: True if the incident existed and was resolved, False otherwise.
        """
        if incident_id in self._incidents:
            self._incidents[incident_id].resolved = True
            return True
        return False

    def reset(self) -> None:
        """Clear all logged incidents (primarily used for test isolation)."""
        self._incidents.clear()


# Process-wide singleton instance.
_manager = IncidentManager()


def get_incident_manager() -> IncidentManager:
    """Retrieve the process-wide IncidentManager singleton.

    Returns:
        IncidentManager: The active incident manager instance.
    """
    return _manager
