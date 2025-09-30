"""Test core data models."""

from datetime import datetime

import pytest

from opengov_earlygerman.core.models import (
    CEFRLevel,
    Formality,
    Gender,
    GermanCase,
    Lesson,
    Noun,
    Student,
    Verb,
    VerbType,
)


def test_cefr_level_enum() -> None:
    """Test CEFR level enumeration."""
    assert CEFRLevel.A1.value == "A1"
    assert CEFRLevel.C2.value == "C2"


def test_german_case_enum() -> None:
    """Test German case enumeration."""
    assert GermanCase.NOMINATIVE.value == "nominative"
    assert GermanCase.DATIVE.value == "dative"


def test_gender_enum() -> None:
    """Test gender enumeration."""
    assert Gender.MASCULINE.value == "masculine"
    assert Gender.FEMININE.value == "feminine"
    assert Gender.NEUTER.value == "neuter"


def test_formality_enum() -> None:
    """Test formality enumeration."""
    assert Formality.FORMAL.value == "formal"
    assert Formality.INFORMAL.value == "informal"


def test_verb_type_enum() -> None:
    """Test verb type enumeration."""
    assert VerbType.WEAK.value == "weak"
    assert VerbType.STRONG.value == "strong"
    assert VerbType.MODAL.value == "modal"


def test_student_model() -> None:
    """Test student model."""
    student = Student(id="1", username="testuser", email="test@example.com")

    assert student.id == "1"
    assert student.username == "testuser"
    assert student.target_level == CEFRLevel.A1
    assert student.current_streak == 0
    assert student.xp_points == 0


def test_student_with_data() -> None:
    """Test student model with data."""
    student = Student(
        id="2",
        username="advanced",
        email="advanced@example.com",
        target_level=CEFRLevel.C1,
        current_streak=30,
        xp_points=5000,
    )

    assert student.target_level == CEFRLevel.C1
    assert student.current_streak == 30
    assert student.xp_points == 5000


def test_noun_model() -> None:
    """Test noun model."""
    noun = Noun(
        id="noun_1",
        word="Mann",
        gender=Gender.MASCULINE,
        english="man",
        pronunciation_ipa="man",
        level=CEFRLevel.A1,
    )

    assert noun.word == "Mann"
    assert noun.gender == Gender.MASCULINE
    assert noun.level == CEFRLevel.A1


def test_verb_model() -> None:
    """Test verb model."""
    verb = Verb(
        id="verb_1",
        infinitive="machen",
        english="to make",
        verb_type=VerbType.WEAK,
        partizip_2="gemacht",
        auxiliary_verb="haben",
        level=CEFRLevel.A1,
    )

    assert verb.infinitive == "machen"
    assert verb.verb_type == VerbType.WEAK
    assert verb.partizip_2 == "gemacht"


def test_verb_separable() -> None:
    """Test separable verb model."""
    verb = Verb(
        id="verb_2",
        infinitive="aufstehen",
        english="to get up",
        verb_type=VerbType.SEPARABLE,
        is_separable=True,
        separable_prefix="auf",
        partizip_2="aufgestanden",
        auxiliary_verb="sein",
        level=CEFRLevel.A1,
    )

    assert verb.is_separable is True
    assert verb.separable_prefix == "auf"


def test_lesson_model() -> None:
    """Test lesson model."""
    lesson = Lesson(
        id="lesson_1",
        title="German Cases Introduction",
        description="Learn about German grammatical cases",
        level=CEFRLevel.A2,
        objectives=["Understand nominative case", "Learn accusative case"],
        duration_minutes=45,
    )

    assert lesson.title == "German Cases Introduction"
    assert lesson.level == CEFRLevel.A2
    assert len(lesson.objectives) == 2
    assert lesson.duration_minutes == 45
