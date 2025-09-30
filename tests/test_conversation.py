"""Test AI conversation partner module."""

import json
from pathlib import Path
from typing import Any, Dict

import pytest

from opengov_earlygerman.ai.conversation import AIConversationPartner
from opengov_earlygerman.core.models import CEFRLevel, Formality


def test_conversation_partner_initialization() -> None:
    """Test conversation partner initialization."""
    partner = AIConversationPartner(level="A1")

    assert partner.level == CEFRLevel.A1
    assert partner.formality == Formality.FORMAL
    assert len(partner.conversation_history) == 0


def test_scenario_defaults() -> None:
    """Test default scenarios are loaded."""
    partner = AIConversationPartner()

    assert "Bäckerei" in partner.available_scenarios()
    assert "Apotheke" in partner.available_scenarios()
    assert "Restaurant" in partner.available_scenarios()


def test_scenario_retrieval() -> None:
    """Test retrieving a specific scenario."""
    partner = AIConversationPartner()
    scenario = partner.scenario("Bäckerei")

    assert "dialogue" in scenario
    assert "english" in scenario
    assert "setting" in scenario
    assert "vocabulary" in scenario
    assert "useful_phrases" in scenario


def test_scenario_not_found() -> None:
    """Test handling of unknown scenario falls back to default."""
    partner = AIConversationPartner()
    scenario = partner.scenario("NonExistent")

    # Falls back to Bäckerei (default) when scenario not found
    assert "bakery" in scenario["setting"].lower() or "bäckerei" in scenario["setting"].lower()


def test_switch_formality() -> None:
    """Test switching between formal and informal."""
    partner = AIConversationPartner()

    # Start formal
    assert partner.formality == Formality.FORMAL

    # Switch to informal
    result = partner.switch_formality(to_informal=True)
    assert partner.formality == Formality.INFORMAL
    assert "du" in result["explanation"]

    # Switch back to formal
    result = partner.switch_formality(to_informal=False)
    assert partner.formality == Formality.FORMAL
    assert "Sie" in result["explanation"]


def test_custom_scenarios_file(tmp_path: Path) -> None:
    """Test loading custom scenarios from JSON file."""
    scenarios_file = tmp_path / "custom_scenarios.json"
    custom_data = {
        "Café": {
            "setting": "You're at a German café",
            "starter": "Was möchten Sie?",
            "english": "What would you like?",
            "vocabulary": {"der Kaffee": "coffee", "der Kuchen": "cake"},
            "useful_phrases": ["Einen Kaffee, bitte - A coffee, please"],
        }
    }

    scenarios_file.write_text(json.dumps(custom_data, ensure_ascii=False), encoding="utf-8")

    partner = AIConversationPartner(scenarios_file=scenarios_file)

    assert "Café" in partner.available_scenarios()
    scenario = partner.scenario("Café")
    assert scenario["setting"] == "You're at a German café"


def test_scenarios_merge(tmp_path: Path) -> None:
    """Test merging custom scenarios with defaults."""
    scenarios_file = tmp_path / "custom_scenarios.json"
    custom_data = {
        "Bäckerei": {
            "vocabulary": {"das Baguette": "baguette"},
        }
    }

    scenarios_file.write_text(json.dumps(custom_data, ensure_ascii=False), encoding="utf-8")

    partner = AIConversationPartner(scenarios_file=scenarios_file)
    scenario = partner.scenario("Bäckerei")

    # Should have both default and custom vocabulary
    assert "das Brötchen" in scenario["vocabulary"]
    assert "das Baguette" in scenario["vocabulary"]


def test_scenarios_merge_with_append_lists(tmp_path: Path) -> None:
    """Test list appending when merging scenarios."""
    scenarios_file = tmp_path / "custom_scenarios.json"
    custom_data = {
        "Bäckerei": {
            "useful_phrases": ["Wie viel kostet das? - How much does that cost?"],
        }
    }

    scenarios_file.write_text(json.dumps(custom_data, ensure_ascii=False), encoding="utf-8")

    partner = AIConversationPartner(scenarios_file=scenarios_file, append_lists=True)
    scenario = partner.scenario("Bäckerei")

    # Should have both default and custom phrases
    phrases = scenario["useful_phrases"]
    assert any("Ich hätte gern" in p for p in phrases)
    assert any("Wie viel kostet das?" in p for p in phrases)


def test_scenarios_merge_replace_lists(tmp_path: Path) -> None:
    """Test list replacement when merging scenarios."""
    scenarios_file = tmp_path / "custom_scenarios.json"
    custom_data = {
        "Bäckerei": {
            "useful_phrases": ["Nur diese eine Phrase"],
        }
    }

    scenarios_file.write_text(json.dumps(custom_data, ensure_ascii=False), encoding="utf-8")

    partner = AIConversationPartner(scenarios_file=scenarios_file, append_lists=False)
    scenario = partner.scenario("Bäckerei")

    # Should only have the custom phrase
    assert scenario["useful_phrases"] == ["Nur diese eine Phrase"]


def test_get_all_scenarios() -> None:
    """Test retrieving all scenarios."""
    partner = AIConversationPartner()
    all_scenarios = partner.get_all_scenarios()

    assert isinstance(all_scenarios, dict)
    assert "Bäckerei" in all_scenarios
    assert "Apotheke" in all_scenarios


def test_scenarios_file_loading_error(tmp_path: Path) -> None:
    """Test handling of invalid JSON file."""
    scenarios_file = tmp_path / "invalid.json"
    scenarios_file.write_text("not valid json", encoding="utf-8")

    # Should fall back to defaults without error
    partner = AIConversationPartner(scenarios_file=scenarios_file)
    assert "Bäckerei" in partner.available_scenarios()


def test_scenarios_file_not_exists(tmp_path: Path) -> None:
    """Test handling of non-existent scenarios file."""
    scenarios_file = tmp_path / "does_not_exist.json"

    # Should fall back to defaults without error
    partner = AIConversationPartner(scenarios_file=scenarios_file)
    assert "Bäckerei" in partner.available_scenarios()


def test_merge_scenarios_with_new_scenario() -> None:
    """Test _merge_scenarios adds new scenarios."""
    partner = AIConversationPartner()
    base: Dict[str, Dict[str, Any]] = {"A": {"x": 1}}
    override: Dict[str, Dict[str, Any]] = {"B": {"y": 2}}

    result = partner._merge_scenarios(base, override)

    assert "A" in result
    assert "B" in result
    assert result["A"]["x"] == 1
    assert result["B"]["y"] == 2


def test_merge_scenarios_nested_dict() -> None:
    """Test _merge_scenarios merges nested dicts."""
    partner = AIConversationPartner()
    base: Dict[str, Dict[str, Any]] = {
        "A": {"vocab": {"word1": "trans1"}}
    }
    override: Dict[str, Dict[str, Any]] = {
        "A": {"vocab": {"word2": "trans2"}}
    }

    result = partner._merge_scenarios(base, override)

    assert result["A"]["vocab"]["word1"] == "trans1"
    assert result["A"]["vocab"]["word2"] == "trans2"