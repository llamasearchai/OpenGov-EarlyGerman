"""FastAPI application for OpenGov-EarlyGerman."""

from typing import Any, Dict

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from opengov_earlygerman import __version__
from opengov_earlygerman.ai.conversation import AIConversationPartner
from opengov_earlygerman.config import settings
from opengov_earlygerman.core.cases_teacher import CasesTeacher
from opengov_earlygerman.core.verb_conjugator import VerbConjugator
from opengov_earlygerman.core.word_order import WordOrderTeacher

app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    description="Comprehensive AI-powered German language learning platform",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize teachers
cases_teacher = CasesTeacher()
verb_conjugator = VerbConjugator()
word_order_teacher = WordOrderTeacher()


class ChatRequest(BaseModel):
    """Chat request model."""

    message: str
    level: str = "A1"


class ConjugateRequest(BaseModel):
    """Conjugate request model."""

    verb: str
    tense: str = "present"


class ArticleRequest(BaseModel):
    """Article practice request model."""

    noun: str
    gender: str = "masculine"


@app.get("/")
async def root() -> Dict[str, str]:
    """Root endpoint."""
    return {
        "name": "OpenGov-EarlyGerman API",
        "version": __version__,
        "description": "AI-powered German language learning platform",
    }


@app.get("/health")
async def health() -> Dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy", "version": __version__}


@app.get("/api/v1/cases/two_way")
async def two_way_prepositions() -> Dict[str, Any]:
    """Get two-way preposition practice."""
    return cases_teacher.practice_two_way_prepositions()


@app.get("/api/v1/cases/{case}")
async def explain_case(case: str) -> Dict[str, Any]:
    """Explain a German grammatical case."""
    try:
        explanation = cases_teacher.explain_case(case)
        if "error" in explanation:
            raise HTTPException(status_code=404, detail=explanation["error"])
        return explanation
    except HTTPException:  # pragma: no cover - pass-through re-raise
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/cases/practice")
async def practice_articles(request: ArticleRequest) -> Dict[str, Any]:
    """Practice article declension."""
    try:
        practice = cases_teacher.practice_articles(request.noun, request.gender)
        if "error" in practice:
            raise HTTPException(status_code=400, detail=practice["error"])
        return practice
    except HTTPException:  # pragma: no cover - pass-through re-raise
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/verbs/conjugate")
async def conjugate_verb(request: ConjugateRequest) -> Dict[str, Any]:
    """Conjugate a German verb."""
    try:
        conjugation = verb_conjugator.conjugate(request.verb, request.tense)
        return conjugation
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/verbs/separable/{verb}")
async def handle_separable_verb(verb: str, sentence_type: str = "main_clause") -> Dict[str, Any]:
    """Handle separable verb."""
    try:
        result = verb_conjugator.handle_separable(verb, sentence_type)
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/word-order/v2")
async def explain_v2_rule() -> Dict[str, Any]:
    """Explain the V2 rule."""
    try:
        return word_order_teacher.explain_v2_rule()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/word-order/subordinate")
async def practice_subordinate() -> Dict[str, Any]:
    """Practice subordinate clause word order."""
    try:
        return word_order_teacher.practice_subordinate_clauses()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/word-order/questions")
async def question_order() -> Dict[str, Any]:
    """Get question word order rules."""
    try:
        return word_order_teacher.question_word_order()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/ai/chat")
async def chat(request: ChatRequest) -> Dict[str, Any]:
    """Chat with AI conversation partner."""
    try:
        partner = AIConversationPartner(level=request.level)
        response = partner.chat(request.message)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/ai/scenario/{scenario_type}")
async def get_scenario(scenario_type: str) -> Dict[str, Any]:
    """Get a conversation scenario."""
    try:
        partner = AIConversationPartner()
        scenario = partner.scenario(scenario_type)
        return scenario
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":  # pragma: no cover - manual run entrypoint
    import uvicorn

    uvicorn.run(app, host=settings.api_host, port=settings.api_port)
