"""Test German cases teaching module."""

import pytest

from opengov_earlygerman.core.cases_teacher import CasesTeacher
from opengov_earlygerman.core.models import Gender, GermanCase


def test_cases_teacher_initialization() -> None:
    """Test cases teacher initialization."""
    teacher = CasesTeacher()

    assert len(teacher.cases) == 4
    assert GermanCase.NOMINATIVE in teacher.cases
    assert GermanCase.DATIVE in teacher.cases


def test_explain_case() -> None:
    """Test case explanation."""
    teacher = CasesTeacher()

    explanation = teacher.explain_case("dative")

    assert "explanation" in explanation
    assert "function" in explanation
    assert "examples" in explanation
    assert "tips" in explanation
    assert "indirect object" in explanation["explanation"].lower()


def test_explain_case_invalid() -> None:
    """Test explaining invalid case."""
    teacher = CasesTeacher()

    explanation = teacher.explain_case("invalid")

    assert "error" in explanation


def test_practice_articles() -> None:
    """Test article declension practice."""
    teacher = CasesTeacher()

    practice = teacher.practice_articles("Mann", "masculine")

    assert "declension_table" in practice
    assert "nominative" in practice["declension_table"]

    # Check correct articles for masculine noun
    nom = practice["declension_table"]["nominative"]
    assert "der Mann" in nom["definite"]

    acc = practice["declension_table"]["accusative"]
    assert "den Mann" in acc["definite"]

    dat = practice["declension_table"]["dative"]
    assert "dem Mann" in dat["definite"]

    gen = practice["declension_table"]["genitive"]
    assert "des Manns" in gen["definite"]


def test_practice_articles_feminine() -> None:
    """Test article declension for feminine noun."""
    teacher = CasesTeacher()

    practice = teacher.practice_articles("Frau", "feminine")

    nom = practice["declension_table"]["nominative"]
    assert "die Frau" in nom["definite"]

    acc = practice["declension_table"]["accusative"]
    assert "die Frau" in acc["definite"]

    dat = practice["declension_table"]["dative"]
    assert "der Frau" in dat["definite"]


def test_practice_articles_neuter() -> None:
    """Test article declension for neuter noun."""
    teacher = CasesTeacher()

    practice = teacher.practice_articles("Buch", "neuter")

    nom = practice["declension_table"]["nominative"]
    assert "das Buch" in nom["definite"]

    acc = practice["declension_table"]["accusative"]
    assert "das Buch" in acc["definite"]

    dat = practice["declension_table"]["dative"]
    assert "dem Buch" in dat["definite"]


def test_practice_articles_genitive_es_ending() -> None:
    teacher = CasesTeacher()
    practice = teacher.practice_articles("Haus", "neuter")
    gen = practice["declension_table"]["genitive"]
    assert "des Hauses" in gen["definite"]


def test_two_way_prepositions() -> None:
    """Test two-way preposition practice."""
    teacher = CasesTeacher()

    practice = teacher.practice_two_way_prepositions()

    assert "explanation" in practice
    assert "examples" in practice
    assert "prepositions" in practice
    assert len(practice["examples"]) > 0
    assert "an" in practice["prepositions"][0]


def test_get_prepositions_for_case() -> None:
    """Test getting prepositions for specific case."""
    teacher = CasesTeacher()

    acc_preps = teacher.get_prepositions_for_case("accusative")
    assert len(acc_preps) > 0
    assert any("durch" in prep for prep in acc_preps)

    dat_preps = teacher.get_prepositions_for_case("dative")
    assert len(dat_preps) > 0
    assert any("mit" in prep for prep in dat_preps)


def test_check_case() -> None:
    """Test case checking functionality."""
    teacher = CasesTeacher()

    result = teacher.check_case("Ich gehe mit dem Mann.", "dem")

    assert "sentence" in result
    assert "your_answer" in result
    assert "correct" in result
    assert "feedback" in result


def test_check_case_accusative_branch() -> None:
    teacher = CasesTeacher()
    result = teacher.check_case("Ich sehe den Mann.", "den")
    assert result["correct"] is True
    assert "accusative" in result["feedback"].lower()


def test_check_case_incorrect_feedback() -> None:
    teacher = CasesTeacher()
    result = teacher.check_case("Hallo Welt.", "xyz")
    assert result["correct"] is False
    assert "Try again" in result["feedback"]
