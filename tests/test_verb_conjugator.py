"""Test German verb conjugation system."""

import pytest

from opengov_earlygerman.core.verb_conjugator import VerbConjugator


def test_weak_verb_conjugation() -> None:
    """Test regular (weak) verb conjugation."""
    conjugator = VerbConjugator()

    result = conjugator.conjugate("machen", tense="present")

    assert result["type"] == "weak"
    assert result["forms"]["ich"] == "mache"
    assert result["forms"]["du"] == "machst"
    assert result["forms"]["er/sie/es"] == "macht"
    assert result["forms"]["wir"] == "machen"


def test_weak_verb_preterite() -> None:
    """Test regular verb preterite conjugation."""
    conjugator = VerbConjugator()

    result = conjugator.conjugate("machen", tense="preterite")

    assert result["type"] == "weak"
    assert result["forms"]["ich"] == "machte"
    assert result["forms"]["du"] == "machtest"
    assert result["forms"]["er/sie/es"] == "machte"


def test_strong_verb_sein() -> None:
    """Test irregular (strong) verb conjugation - sein."""
    conjugator = VerbConjugator()

    result = conjugator.conjugate("sein", tense="present")

    assert result["type"] == "strong"
    assert result["forms"]["ich"] == "bin"
    assert result["forms"]["du"] == "bist"
    assert result["forms"]["er/sie/es"] == "ist"
    assert result["forms"]["wir"] == "sind"


def test_strong_verb_haben() -> None:
    """Test irregular (strong) verb conjugation - haben."""
    conjugator = VerbConjugator()

    result = conjugator.conjugate("haben", tense="present")

    assert result["type"] == "strong"
    assert result["forms"]["ich"] == "habe"
    assert result["forms"]["du"] == "hast"
    assert result["forms"]["er/sie/es"] == "hat"


def test_modal_verb_können() -> None:
    """Test modal verb conjugation - können."""
    conjugator = VerbConjugator()

    result = conjugator.conjugate("können", tense="present")

    assert result["type"] == "modal"
    assert result["forms"]["ich"] == "kann"
    assert result["forms"]["du"] == "kannst"
    assert result["forms"]["er/sie/es"] == "kann"


def test_modal_verb_müssen() -> None:
    """Test modal verb conjugation - müssen."""
    conjugator = VerbConjugator()

    result = conjugator.conjugate("müssen", tense="present")

    assert result["type"] == "modal"
    assert result["forms"]["ich"] == "muss"
    assert result["forms"]["du"] == "musst"


def test_separable_verb() -> None:
    """Test separable verb handling."""
    conjugator = VerbConjugator()

    result = conjugator.handle_separable("aufstehen", "main_clause")

    assert result["prefix"] == "auf"
    assert result["base_verb"] == "stehen"
    assert "examples" in result
    assert len(result["examples"]) > 0


def test_separable_verb_subordinate() -> None:
    """Test separable verb in subordinate clause."""
    conjugator = VerbConjugator()

    result = conjugator.handle_separable("aufstehen", "subordinate_clause")

    assert result["prefix"] == "auf"
    assert result["sentence_type"] == "subordinate_clause"


def test_non_separable_verb() -> None:
    """Test non-separable verb handling."""
    conjugator = VerbConjugator()

    result = conjugator.handle_separable("machen", "main_clause")

    assert "error" in result


def test_modal_with_main_verb() -> None:
    """Test modal verb with main verb combination."""
    conjugator = VerbConjugator()

    result = conjugator.with_modal("können", "schwimmen")

    assert result["modal"] == "können"
    assert result["main_verb"] == "schwimmen"
    assert "conjugation" in result
    assert result["conjugation"]["ich"] == "kann"
    assert "examples" in result


def test_modal_translation() -> None:
    """Test modal verb translation."""
    conjugator = VerbConjugator()

    result = conjugator.with_modal("wollen", "gehen")

    assert "examples" in result
    assert any("want to" in ex["english"] for ex in result["examples"])


def test_get_stem() -> None:
    """Test stem extraction."""
    conjugator = VerbConjugator()

    assert conjugator._get_stem("machen") == "mach"
    assert conjugator._get_stem("gehen") == "geh"
    assert conjugator._get_stem("sein") == "sei"
    assert conjugator._get_stem("mach") == "mach"


def test_regular_verb_e_insertion() -> None:
    conjugator = VerbConjugator()
    res = conjugator.conjugate("arbeiten", tense="present")
    # "du arbeitest" requires an 'e' insertion
    assert res["forms"]["du"] == "arbeitest"
