"""Test German word order teaching module."""

import pytest

from opengov_earlygerman.core.word_order import WordOrderTeacher


def test_word_order_initialization() -> None:
    """Test word order teacher initialization."""
    teacher = WordOrderTeacher()

    assert "v2_rule" in teacher.rules
    assert "time_manner_place" in teacher.rules
    assert "subordinate_clause" in teacher.rules


def test_explain_v2_rule() -> None:
    """Test V2 rule explanation."""
    teacher = WordOrderTeacher()

    explanation = teacher.explain_v2_rule()

    assert "rule" in explanation
    assert "practice" in explanation
    assert "exceptions" in explanation
    assert "tip" in explanation


def test_v2_rule_examples() -> None:
    """Test V2 rule has proper examples."""
    teacher = WordOrderTeacher()

    v2 = teacher.explain_v2_rule()

    assert len(v2["rule"]["examples"]) >= 3
    assert any("Heute" in ex["german"] for ex in v2["rule"]["examples"])


def test_arrange_elements_basic() -> None:
    """Test arranging sentence elements."""
    teacher = WordOrderTeacher()

    result = teacher.arrange_elements(subject="Ich", verb="gehe", place="nach Hause")

    assert "correct_order" in result
    assert "variations" in result
    assert "Ich gehe nach Hause" in result["correct_order"]


def test_arrange_elements_tmp() -> None:
    """Test TMP order arrangement."""
    teacher = WordOrderTeacher()

    result = teacher.arrange_elements(
        subject="Ich", verb="fahre", time="morgen", manner="mit dem Zug", place="nach Berlin"
    )

    assert "correct_order" in result
    assert "morgen" in result["correct_order"]
    assert "mit dem Zug" in result["correct_order"]
    assert "nach Berlin" in result["correct_order"]


def test_arrange_elements_variations() -> None:
    """Test sentence variations."""
    teacher = WordOrderTeacher()

    result = teacher.arrange_elements(subject="Ich", verb="gehe", time="heute", place="ins Kino")

    assert len(result["variations"]) >= 1
    assert any("heute" in var for var in result["variations"])


def test_arrange_elements_with_direct_object() -> None:
    teacher = WordOrderTeacher()
    res = teacher.arrange_elements(
        subject="Ich", verb="sehe", direct_object="den Mann", time="heute", place="im Park"
    )
    assert "den Mann" in res["correct_order"]
    # Ensure variations include direct object
    assert any("den Mann" in var for var in res["variations"])


def test_practice_subordinate_clauses() -> None:
    """Test subordinate clause practice."""
    teacher = WordOrderTeacher()

    practice = teacher.practice_subordinate_clauses()

    assert "rule" in practice
    assert "structure" in practice
    assert "examples" in practice
    assert len(practice["examples"]) >= 2


def test_subordinate_clause_examples() -> None:
    """Test subordinate clause examples are valid."""
    teacher = WordOrderTeacher()

    practice = teacher.practice_subordinate_clauses()

    for example in practice["examples"]:
        assert "main" in example
        assert "subordinate" in example
        assert "complete" in example
        assert "english" in example


def test_question_word_order() -> None:
    """Test question word order explanation."""
    teacher = WordOrderTeacher()

    questions = teacher.question_word_order()

    assert "yes_no_questions" in questions
    assert "w_questions" in questions


def test_yes_no_questions() -> None:
    """Test yes/no question structure."""
    teacher = WordOrderTeacher()

    questions = teacher.question_word_order()

    assert "rule" in questions["yes_no_questions"]
    assert "examples" in questions["yes_no_questions"]
    assert len(questions["yes_no_questions"]["examples"]) > 0


def test_w_questions() -> None:
    """Test W-question structure."""
    teacher = WordOrderTeacher()

    questions = teacher.question_word_order()

    assert "w_words" in questions["w_questions"]
    assert "wer" in questions["w_questions"]["w_words"]
    assert "was" in questions["w_questions"]["w_words"]


def test_connectors() -> None:
    """Test connector initialization."""
    teacher = WordOrderTeacher()

    assert "coordinating" in teacher.connectors
    assert "subordinating" in teacher.connectors
    assert "two_part" in teacher.connectors
