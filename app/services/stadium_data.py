from __future__ import annotations

import json
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Any

_DATA_DIR = Path(__file__).resolve().parent.parent / "data"

I18n = dict[str, str]
_DEFAULT_LANG = "en"


def localized(mapping: I18n | None, language: str) -> str | None:
    """Retrieve the localized string from a dictionary mapping.

    Falls back to English if the requested language is missing, then to the first available key.

    Args:
        mapping: Dictionary mapping language codes (e.g. 'en', 'es') to strings.
        language: Target language code.

    Returns:
        Optional[str]: The localized string, or None if the mapping is empty/None.
    """
    if not mapping:
        return None
    return mapping.get(language) or mapping.get(_DEFAULT_LANG) or next(iter(mapping.values()))


@dataclass
class Zone:
    """Represents a structural zone or area of the stadium layout.

    Attributes:
        id: Unique alphanumeric identifier.
        names: Localized name dictionary.
        type: The category of the zone ("gate", "concourse", "seating").
        level: Stadium level description.
    """
    id: str
    names: I18n
    type: str
    level: str


@dataclass(frozen=True)
class Edge:
    """Represents a connection between two stadium zones.

    Attributes:
        to: Destination zone ID.
        means: Traversal mode ("walk", "ramp", "elevator", "stairs").
        step_free: True if wheelchair/step-free accessible.
        distance: Distance in meters.
    """
    to: str
    means: str
    step_free: bool
    distance: int


@dataclass
class Facility:
    """Represents a stadium service amenity or point of interest.

    Attributes:
        id: Unique identifier for the facility.
        names: Localized name map.
        type: Type category (e.g. "restroom", "first_aid", "concession").
        zone: Zone ID where the facility resides.
        accessible: True if wheelchair-accessible.
        landmarks: Localized landmark direction hints.
    """
    id: str
    names: I18n
    type: str
    zone: str
    accessible: bool
    landmarks: I18n | None = None


@dataclass
class Stadium:
    """In-memory layout database of MetLife Stadium.

    Holds records of zones, adjacency lists, and facilities, loaded from JSON fixtures.
    """
    name: str
    fifa_name: str
    city: str
    capacity: int
    zones: dict[str, Zone]
    adjacency: dict[str, list[Edge]]
    facilities: list[Facility]
    crowd_base: dict[str, str]
    crowd_sim: dict[str, Any] = field(default_factory=dict)

    def zone_ids(self) -> frozenset[str]:
        """Fetch the set of all valid zone identifiers.

        Returns:
            frozenset[str]: Frozenset of zone ID strings.
        """
        return frozenset(self.zones)

    def zone_name(self, zone_id: str, language: str = _DEFAULT_LANG) -> str:
        """Resolve the localized name of a zone.

        Args:
            zone_id: The zone ID.
            language: Target language code.

        Returns:
            str: Localized name, or the raw zone_id if missing.
        """
        zone = self.zones.get(zone_id)
        return (localized(zone.names, language) or zone_id) if zone else zone_id

    def zone_type(self, zone_id: str) -> str:
        """Get the type category of a zone.

        Args:
            zone_id: The zone ID.

        Returns:
            str: Zone type category (e.g., "gate"), or empty string if not found.
        """
        zone = self.zones.get(zone_id)
        return zone.type if zone else ""

    def neighbors(self, zone_id: str) -> list[Edge]:
        """Get all outgoing edge connections for a given zone.

        Args:
            zone_id: Starting zone ID.

        Returns:
            list[Edge]: List of edge connections.
        """
        return self.adjacency.get(zone_id, [])

    def facilities_of_types(
        self, types: set[str], *, accessible_only: bool = False
    ) -> list[Facility]:
        """Search and filter facilities by category types and accessibility.

        Args:
            types: Set of facility type strings to query.
            accessible_only: If True, filters out non-accessible facilities.

        Returns:
            list[Facility]: Match list of facility objects.
        """
        return [
            f
            for f in self.facilities
            if f.type in types and (f.accessible or not accessible_only)
        ]

    def base_crowd(self, zone_id: str) -> str:
        """Fetch the baseline crowd level for a zone from static schedules.

        Args:
            zone_id: The zone ID.

        Returns:
            str: Baseline crowd level ("low", "medium", or "high").
        """
        return self.crowd_base.get(zone_id, "low")


def _read_json(filename: str) -> dict[str, Any]:
    """Helper to read and parse a UTF-8 JSON file from the data directory.

    Args:
        filename: Name of the JSON file.

    Returns:
        dict[str, Any]: Parsed JSON dictionary content.
    """
    with (_DATA_DIR / filename).open(encoding="utf-8") as fh:
        data = json.load(fh)
        if not isinstance(data, dict):
            raise TypeError("Data must be a JSON object")  # pragma: no cover
        return data


def _build_stadium() -> Stadium:
    """Assemble the Stadium database singleton from JSON data fixtures.

    Returns:
        Stadium: Configured Stadium instance.
    """
    stadium_raw = _read_json("stadium.json")
    facilities_raw = _read_json("facilities.json")
    crowd_raw = _read_json("crowd.json")

    zones = {
        z["id"]: Zone(id=z["id"], names=z["name"], type=z["type"], level=z["level"])
        for z in stadium_raw["zones"]
    }

    adjacency: dict[str, list[Edge]] = {zid: [] for zid in zones}
    for e in stadium_raw["edges"]:
        src, dst = e["from"], e["to"]
        adjacency[src].append(
            Edge(to=dst, means=e["means"], step_free=e["step_free"], distance=e["distance"])
        )
        adjacency[dst].append(
            Edge(to=src, means=e["means"], step_free=e["step_free"], distance=e["distance"])
        )

    facilities = [
        Facility(
            id=f["id"],
            names=f["name"],
            type=f["type"],
            zone=f["zone"],
            accessible=f["accessible"],
            landmarks=f.get("landmark"),
        )
        for f in facilities_raw["facilities"]
    ]

    meta = stadium_raw["stadium"]
    return Stadium(
        name=meta["name"],
        fifa_name=meta["fifa_name"],
        city=meta["city"],
        capacity=meta["capacity"],
        zones=zones,
        adjacency=adjacency,
        facilities=facilities,
        crowd_base=dict(crowd_raw["base"]),
        crowd_sim=dict(crowd_raw.get("simulation", {})),
    )


@lru_cache(maxsize=1)
def get_stadium() -> Stadium:
    """Retrieve the cached Stadium database instance.

    Returns:
        Stadium: The initialized MetLife Stadium database cache.
    """
    return _build_stadium()
