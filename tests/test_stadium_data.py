from __future__ import annotations

from app.services.stadium_data import get_stadium, localized


def test_localized_helper():
    # Helper should resolve correctly
    assert localized({"en": "Hello", "es": "Hola"}, "es") == "Hola"
    assert localized({"en": "Hello", "es": "Hola"}, "fr") == "Hello"
    assert localized(None, "en") is None


def test_stadium_singleton_metadata():
    stadium = get_stadium()
    assert stadium.name == "MetLife Stadium"
    assert stadium.capacity == 82500
    assert "gate_a" in stadium.zone_ids()


def test_zone_name_and_type():
    stadium = get_stadium()
    assert stadium.zone_name("gate_a", "en") == "Gate A (South-West)"
    assert stadium.zone_name("gate_a", "es") == "Puerta A (suroeste)"
    assert stadium.zone_type("gate_a") == "gate"
    assert stadium.zone_type("unknown") == ""


def test_facilities_by_type():
    stadium = get_stadium()
    first_aids = stadium.facilities_of_types({"first_aid"})
    assert len(first_aids) == 2
    assert all(f.type == "first_aid" for f in first_aids)

    # Accessible restrooms only
    accessible = stadium.facilities_of_types({"accessible_restroom"}, accessible_only=True)
    assert len(accessible) == 2
    assert all(f.accessible for f in accessible)


def test_base_crowd():
    stadium = get_stadium()
    assert stadium.base_crowd("gate_a") == "medium"
    assert stadium.base_crowd("unknown") == "low"
