"""Test FastAPI application."""

import pytest
from fastapi.testclient import TestClient

from opengov_earlygerman.api.main import app

client = TestClient(app)


def test_root() -> None:
    """Test root endpoint."""
    response = client.get("/")

    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "version" in data


def test_health() -> None:
    """Test health check endpoint."""
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data


def test_explain_case() -> None:
    """Test case explanation endpoint."""
    response = client.get("/api/v1/cases/dative")

    assert response.status_code == 200
    data = response.json()
    assert "explanation" in data
    assert "function" in data
    assert "examples" in data


def test_explain_case_invalid() -> None:
    """Test invalid case endpoint."""
    response = client.get("/api/v1/cases/invalid")

    assert response.status_code == 404


def test_practice_articles() -> None:
    """Test article practice endpoint."""
    response = client.post(
        "/api/v1/cases/practice", json={"noun": "Mann", "gender": "masculine"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "declension_table" in data
    assert "nominative" in data["declension_table"]


def test_practice_articles_invalid_gender() -> None:
    response = client.post(
        "/api/v1/cases/practice", json={"noun": "Mann", "gender": "invalid"}
    )
    assert response.status_code == 400


def test_two_way_prepositions() -> None:
    """Test two-way prepositions endpoint."""
    response = client.get("/api/v1/cases/two_way")

    assert response.status_code == 200
    data = response.json()
    assert "explanation" in data
    assert "examples" in data


def test_conjugate_verb() -> None:
    """Test verb conjugation endpoint."""
    response = client.post("/api/v1/verbs/conjugate", json={"verb": "machen", "tense": "present"})

    assert response.status_code == 200
    data = response.json()
    assert "forms" in data
    assert "type" in data


def test_separable_verb() -> None:
    """Test separable verb endpoint."""
    response = client.get("/api/v1/verbs/separable/aufstehen")

    assert response.status_code == 200
    data = response.json()
    assert "prefix" in data
    assert "base_verb" in data


def test_separable_verb_error() -> None:
    response = client.get("/api/v1/verbs/separable/machen")
    assert response.status_code == 400


def test_v2_rule() -> None:
    """Test V2 rule endpoint."""
    response = client.get("/api/v1/word-order/v2")

    assert response.status_code == 200
    data = response.json()
    assert "rule" in data
    assert "practice" in data


def test_subordinate_clauses() -> None:
    """Test subordinate clause endpoint."""
    response = client.get("/api/v1/word-order/subordinate")

    assert response.status_code == 200
    data = response.json()
    assert "rule" in data
    assert "examples" in data


def test_question_order() -> None:
    """Test question word order endpoint."""
    response = client.get("/api/v1/word-order/questions")

    assert response.status_code == 200
    data = response.json()
    assert "yes_no_questions" in data
    assert "w_questions" in data


def test_chat_endpoint_success(monkeypatch: pytest.MonkeyPatch) -> None:
    class DummyPartner:
        def __init__(self, level: str = "A1") -> None:
            pass

        def chat(self, msg: str) -> dict:
            return {"german": "Hallo", "english": "Hello"}

    from opengov_earlygerman import api

    monkeypatch.setattr(api.main, "AIConversationPartner", DummyPartner)
    response = client.post("/api/v1/ai/chat", json={"message": "hi", "level": "A1"})
    assert response.status_code == 200
    assert response.json()["german"] == "Hallo"


def test_chat_endpoint_error(monkeypatch: pytest.MonkeyPatch) -> None:
    class DummyPartner:
        def __init__(self, level: str = "A1") -> None:
            pass

        def chat(self, msg: str) -> dict:  # type: ignore[override]
            raise RuntimeError("boom")

    from opengov_earlygerman import api

    monkeypatch.setattr(api.main, "AIConversationPartner", DummyPartner)
    response = client.post("/api/v1/ai/chat", json={"message": "hi", "level": "A1"})
    assert response.status_code == 500


def test_scenario() -> None:
    """Test scenario endpoint."""
    response = client.get("/api/v1/ai/scenario/Bäckerei")

    assert response.status_code == 200
    data = response.json()
    assert "dialogue" in data
    assert "vocabulary" in data
    assert "useful_phrases" in data


def test_explain_case_exception(monkeypatch: pytest.MonkeyPatch) -> None:
    from opengov_earlygerman import api

    def boom(case: str):  # type: ignore[override]
        raise RuntimeError("fail")

    monkeypatch.setattr(api.main.cases_teacher, "explain_case", boom)
    response = client.get("/api/v1/cases/nominative")
    assert response.status_code == 500


def test_practice_articles_exception(monkeypatch: pytest.MonkeyPatch) -> None:
    from opengov_earlygerman import api

    def boom(noun: str, gender: str):  # type: ignore[override]
        raise RuntimeError("fail")

    monkeypatch.setattr(api.main.cases_teacher, "practice_articles", boom)
    response = client.post(
        "/api/v1/cases/practice", json={"noun": "Mann", "gender": "masculine"}
    )
    assert response.status_code == 500


def test_conjugate_exception(monkeypatch: pytest.MonkeyPatch) -> None:
    from opengov_earlygerman import api

    def boom(verb: str, tense: str):  # type: ignore[override]
        raise RuntimeError("fail")

    monkeypatch.setattr(api.main.verb_conjugator, "conjugate", boom)
    response = client.post(
        "/api/v1/verbs/conjugate", json={"verb": "machen", "tense": "present"}
    )
    assert response.status_code == 500


def test_separable_exception(monkeypatch: pytest.MonkeyPatch) -> None:
    from opengov_earlygerman import api

    def boom(verb: str, sentence_type: str):  # type: ignore[override]
        raise RuntimeError("fail")

    monkeypatch.setattr(api.main.verb_conjugator, "handle_separable", boom)
    response = client.get("/api/v1/verbs/separable/aufstehen")
    assert response.status_code == 500


def test_wordorder_v2_exception(monkeypatch: pytest.MonkeyPatch) -> None:
    from opengov_earlygerman import api

    def boom():  # type: ignore[override]
        raise RuntimeError("fail")

    monkeypatch.setattr(api.main.word_order_teacher, "explain_v2_rule", boom)
    response = client.get("/api/v1/word-order/v2")
    assert response.status_code == 500


def test_wordorder_subordinate_exception(monkeypatch: pytest.MonkeyPatch) -> None:
    from opengov_earlygerman import api

    def boom():  # type: ignore[override]
        raise RuntimeError("fail")

    monkeypatch.setattr(api.main.word_order_teacher, "practice_subordinate_clauses", boom)
    response = client.get("/api/v1/word-order/subordinate")
    assert response.status_code == 500


def test_wordorder_questions_exception(monkeypatch: pytest.MonkeyPatch) -> None:
    from opengov_earlygerman import api

    def boom():  # type: ignore[override]
        raise RuntimeError("fail")

    monkeypatch.setattr(api.main.word_order_teacher, "question_word_order", boom)
    response = client.get("/api/v1/word-order/questions")
    assert response.status_code == 500


def test_scenario_exception(monkeypatch: pytest.MonkeyPatch) -> None:
    from opengov_earlygerman import api

    class Dummy:
        def scenario(self, name: str):  # type: ignore[override]
            raise RuntimeError("fail")

    monkeypatch.setattr(api.main, "AIConversationPartner", lambda: Dummy())
    response = client.get("/api/v1/ai/scenario/Apotheke")
    assert response.status_code == 500
