"""Core data models for German language learning."""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class CEFRLevel(str, Enum):
    """CEFR proficiency levels."""

    A1 = "A1"
    A2 = "A2"
    B1 = "B1"
    B2 = "B2"
    C1 = "C1"
    C2 = "C2"


class GermanCase(str, Enum):
    """German grammatical cases."""

    NOMINATIVE = "nominative"
    ACCUSATIVE = "accusative"
    DATIVE = "dative"
    GENITIVE = "genitive"


class Gender(str, Enum):
    """German grammatical genders."""

    MASCULINE = "masculine"
    FEMININE = "feminine"
    NEUTER = "neuter"
    PLURAL = "plural"


class Formality(str, Enum):
    """Formality levels."""

    INFORMAL = "informal"
    FORMAL = "formal"


class VerbType(str, Enum):
    """German verb types."""

    WEAK = "weak"
    STRONG = "strong"
    MIXED = "mixed"
    MODAL = "modal"
    SEPARABLE = "separable"
    REFLEXIVE = "reflexive"


class Student(BaseModel):
    """Student model."""

    id: str = Field(description="Student ID")
    username: str = Field(description="Username")
    email: str = Field(description="Email address")
    native_language: str = Field(default="en", description="Native language code")
    target_level: CEFRLevel = Field(default=CEFRLevel.A1)
    current_level: Optional[CEFRLevel] = None

    learning_goals: List[str] = Field(default_factory=list)
    daily_goal_minutes: int = Field(default=30)

    total_study_time: int = Field(default=0, description="Total minutes studied")
    current_streak: int = Field(default=0, description="Current day streak")
    longest_streak: int = Field(default=0)
    xp_points: int = Field(default=0)
    achievements: List[str] = Field(default_factory=list)

    cases_mastered: Dict[str, float] = Field(default_factory=dict)
    vocabulary_known: int = Field(default=0)
    verbs_mastered: int = Field(default=0)

    preferences: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_study_date: Optional[datetime] = None


class Noun(BaseModel):
    """German noun model."""

    id: str = Field(description="Noun ID")
    word: str = Field(description="German word")
    gender: Gender = Field(description="Grammatical gender")
    english: str = Field(description="English translation")

    plural: Optional[str] = Field(default=None, description="Plural form")

    declensions: Dict[str, str] = Field(
        default_factory=dict, description="Declensions by case"
    )

    pronunciation_ipa: str = Field(description="IPA pronunciation")
    audio_url: Optional[str] = None

    example_sentences: List[Dict[str, str]] = Field(default_factory=list)
    compounds: List[str] = Field(default_factory=list, description="Common compounds")

    level: CEFRLevel = Field(description="CEFR level")
    frequency_rank: Optional[int] = None

    semantic_field: Optional[str] = None
    gender_pattern: Optional[str] = None


class Verb(BaseModel):
    """German verb model."""

    id: str = Field(description="Verb ID")
    infinitive: str = Field(description="Infinitive form")
    english: str = Field(description="English translation")
    verb_type: VerbType = Field(description="Verb type")

    is_separable: bool = Field(default=False)
    separable_prefix: Optional[str] = None

    is_reflexive: bool = Field(default=False)
    reflexive_pronoun_case: Optional[GermanCase] = None

    conjugations: Dict[str, Dict[str, str]] = Field(
        default_factory=dict, description="Conjugations by tense and person"
    )

    partizip_2: str = Field(description="Past participle")
    auxiliary_verb: str = Field(description="haben or sein")

    imperative: Dict[str, str] = Field(default_factory=dict)

    example_sentences: List[Dict[str, str]] = Field(default_factory=list)

    level: CEFRLevel = Field(description="CEFR level")
    frequency_rank: Optional[int] = None


class Lesson(BaseModel):
    """Lesson model."""

    id: str = Field(description="Lesson ID")
    title: str = Field(description="Lesson title")
    description: str = Field(description="Lesson description")
    level: CEFRLevel = Field(description="CEFR level")

    objectives: List[str] = Field(description="Learning objectives")
    duration_minutes: int = Field(description="Estimated duration")

    grammar_points: List[str] = Field(default_factory=list)
    vocabulary: List[str] = Field(default_factory=list)

    exercises: List[Dict[str, Any]] = Field(default_factory=list)

    prerequisites: List[str] = Field(default_factory=list)
    next_lessons: List[str] = Field(default_factory=list)

    created_at: datetime = Field(default_factory=datetime.utcnow)
