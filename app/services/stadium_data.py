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
    if not mapping:
        return None
    return mapping.get(language) or mapping.get(_DEFAULT_LANG) or next(iter(mapping.values()))


@dataclass
class Zone:
    id: str
    names: I18n
    type: str  # "gate" | "concourse" | "seating"
    level: str


@dataclass(frozen=True)
class Edge:
    to: str
    means: str  # "walk" | "ramp" | "elevator" | "stairs"
    step_free: bool
    distance: int


@dataclass
class Facility:
    id: str
    names: I18n
    type: str
    zone: str
    accessible: bool
    landmarks: I18n | None = None


@dataclass
class Stadium:
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
        return frozenset(self.zones)

    def zone_name(self, zone_id: str, language: str = _DEFAULT_LANG) -> str:
        zone = self.zones.get(zone_id)
        return (localized(zone.names, language) or zone_id) if zone else zone_id

    def zone_type(self, zone_id: str) -> str:
        zone = self.zones.get(zone_id)
        return zone.type if zone else ""

    def neighbors(self, zone_id: str) -> list[Edge]:
        return self.adjacency.get(zone_id, [])

    def facilities_of_types(
        self, types: set[str], *, accessible_only: bool = False
    ) -> list[Facility]:
        return [
            f
            for f in self.facilities
            if f.type in types and (f.accessible or not accessible_only)
        ]

    def base_crowd(self, zone_id: str) -> str:
        return self.crowd_base.get(zone_id, "low")


def _read_json(filename: str) -> dict[str, Any]:
    with (_DATA_DIR / filename).open(encoding="utf-8") as fh:
        data = json.load(fh)
        if not isinstance(data, dict):
            raise TypeError("Data must be a JSON object")  # pragma: no cover
        return data


def _build_stadium() -> Stadium:
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
    return _build_stadium()
