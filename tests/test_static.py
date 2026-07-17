from __future__ import annotations

from pathlib import Path

import app

_HTML = (Path(app.__file__).resolve().parent / "static" / "index.html").read_text(encoding="utf-8")


def test_document_has_lang_attribute():
    assert '<html lang="en">' in _HTML


def test_single_h1_and_landmarks():
    assert _HTML.count("<h1") == 1
    for landmark in ("<header", "<nav", "<main", "<footer"):
        assert landmark in _HTML


def test_live_region_and_skip_link():
    assert 'aria-live="polite"' in _HTML
    assert 'class="skip-link"' in _HTML and 'href="#main"' in _HTML


def test_toggle_exposes_pressed_state():
    assert 'id="contrast-toggle"' in _HTML and 'aria-pressed="false"' in _HTML
    assert 'id="persona-toggle"' in _HTML and 'aria-pressed="false"' in _HTML


def test_form_controls_have_associated_labels():
    for control_id in ("language", "current_location", "destination_intent",
                       "ticket_section", "minutes_to_kickoff", "question"):
        assert f'id="{control_id}"' in _HTML
        assert f'for="{control_id}"' in _HTML
    assert "<fieldset" in _HTML and "<legend" in _HTML


def test_three_languages_offered():
    for value in ('value="en"', 'value="es"', 'value="fr"'):
        assert value in _HTML
