"""German cases teaching module."""

from typing import Any, Dict, List

from opengov_earlygerman.core.models import Gender, GermanCase
from opengov_earlygerman.utils.logger import get_logger

logger = get_logger(__name__)


class CasesTeacher:
    """Teaches German grammatical cases."""

    def __init__(self) -> None:
        """Initialize cases teacher."""
        self.cases = self._initialize_cases()
        self.articles = self._initialize_articles()
        self.prepositions = self._initialize_prepositions()

    def _initialize_cases(self) -> Dict[GermanCase, Dict[str, Any]]:
        """Initialize case explanations and examples."""
        return {
            GermanCase.NOMINATIVE: {
                "name": "Nominativ",
                "function": "Subject of the sentence",
                "question": "Wer? Was? (Who? What?)",
                "explanation": "The nominative case marks the subject - the person or thing doing the action",
                "examples": [
                    {
                        "german": "Der Mann liest ein Buch.",
                        "english": "The man reads a book.",
                        "highlight": "Der Mann",
                    },
                    {
                        "german": "Die Frau ist Ärztin.",
                        "english": "The woman is a doctor.",
                        "highlight": "Die Frau",
                    },
                ],
                "tips": [
                    "The subject usually comes first (but not always in German!)",
                    "After 'sein' (to be), use nominative",
                    "Ask 'Who is doing the action?' to find the nominative",
                ],
            },
            GermanCase.ACCUSATIVE: {
                "name": "Akkusativ",
                "function": "Direct object of the sentence",
                "question": "Wen? Was? (Whom? What?)",
                "explanation": "The accusative case marks the direct object - what is being acted upon",
                "examples": [
                    {
                        "german": "Ich sehe den Mann.",
                        "english": "I see the man.",
                        "highlight": "den Mann",
                    },
                    {
                        "german": "Sie kauft einen Apfel.",
                        "english": "She buys an apple.",
                        "highlight": "einen Apfel",
                    },
                ],
                "tips": [
                    "Only masculine articles change in accusative (der → den, ein → einen)",
                    "Most verbs take accusative objects",
                    "Motion towards something often uses accusative",
                ],
            },
            GermanCase.DATIVE: {
                "name": "Dativ",
                "function": "Indirect object of the sentence",
                "question": "Wem? (To/For whom?)",
                "explanation": "The dative case marks the indirect object - to whom or for whom",
                "examples": [
                    {
                        "german": "Ich gebe dem Mann das Buch.",
                        "english": "I give the man the book.",
                        "highlight": "dem Mann",
                    },
                    {
                        "german": "Sie hilft der Frau.",
                        "english": "She helps the woman.",
                        "highlight": "der Frau",
                    },
                ],
                "tips": [
                    "Dative plural always adds -n to the noun (if not already there)",
                    "Some verbs always take dative (helfen, danken, folgen)",
                    "Location (without movement) uses dative",
                ],
            },
            GermanCase.GENITIVE: {
                "name": "Genitiv",
                "function": "Shows possession or relationship",
                "question": "Wessen? (Whose?)",
                "explanation": "The genitive case shows possession or close relationship",
                "examples": [
                    {
                        "german": "Das ist das Auto des Mannes.",
                        "english": "That is the man's car.",
                        "highlight": "des Mannes",
                    },
                    {
                        "german": "Die Tür des Hauses ist blau.",
                        "english": "The door of the house is blue.",
                        "highlight": "des Hauses",
                    },
                ],
                "tips": [
                    "Masculine and neuter nouns add -(e)s in genitive",
                    "Genitive is becoming less common in spoken German",
                    "Often replaced by 'von + dative' in casual speech",
                ],
            },
        }

    def _initialize_articles(self) -> Dict[str, Dict[GermanCase, Dict[Gender, str]]]:
        """Initialize definite and indefinite articles by case and gender."""
        return {
            "definite": {
                GermanCase.NOMINATIVE: {
                    Gender.MASCULINE: "der",
                    Gender.FEMININE: "die",
                    Gender.NEUTER: "das",
                    Gender.PLURAL: "die",
                },
                GermanCase.ACCUSATIVE: {
                    Gender.MASCULINE: "den",
                    Gender.FEMININE: "die",
                    Gender.NEUTER: "das",
                    Gender.PLURAL: "die",
                },
                GermanCase.DATIVE: {
                    Gender.MASCULINE: "dem",
                    Gender.FEMININE: "der",
                    Gender.NEUTER: "dem",
                    Gender.PLURAL: "den",
                },
                GermanCase.GENITIVE: {
                    Gender.MASCULINE: "des",
                    Gender.FEMININE: "der",
                    Gender.NEUTER: "des",
                    Gender.PLURAL: "der",
                },
            },
            "indefinite": {
                GermanCase.NOMINATIVE: {
                    Gender.MASCULINE: "ein",
                    Gender.FEMININE: "eine",
                    Gender.NEUTER: "ein",
                },
                GermanCase.ACCUSATIVE: {
                    Gender.MASCULINE: "einen",
                    Gender.FEMININE: "eine",
                    Gender.NEUTER: "ein",
                },
                GermanCase.DATIVE: {
                    Gender.MASCULINE: "einem",
                    Gender.FEMININE: "einer",
                    Gender.NEUTER: "einem",
                },
                GermanCase.GENITIVE: {
                    Gender.MASCULINE: "eines",
                    Gender.FEMININE: "einer",
                    Gender.NEUTER: "eines",
                },
            },
        }

    def _initialize_prepositions(self) -> Dict[str, List[str]]:
        """Initialize prepositions by case."""
        return {
            "accusative": [
                "durch (through)",
                "für (for)",
                "gegen (against)",
                "ohne (without)",
                "um (around)",
            ],
            "dative": [
                "aus (from/out of)",
                "bei (at/with)",
                "mit (with)",
                "nach (after/to)",
                "seit (since)",
                "von (from/of)",
                "zu (to)",
            ],
            "genitive": [
                "während (during)",
                "wegen (because of)",
                "trotz (despite)",
                "statt (instead of)",
            ],
            "two_way": [
                "an (at/on)",
                "auf (on)",
                "hinter (behind)",
                "in (in)",
                "neben (next to)",
                "über (over)",
                "unter (under)",
                "vor (in front of)",
                "zwischen (between)",
            ],
        }

    def explain_case(self, case: str) -> Dict[str, Any]:
        """Explain a specific case."""
        try:
            case_enum = GermanCase(case.lower())
        except ValueError:
            return {"error": f"Case {case} not found"}

        if case_enum not in self.cases:  # pragma: no cover - defensive guard
            return {"error": f"Case {case} not found"}

        return {
            "case": case,
            "explanation": self.cases[case_enum]["explanation"],
            "function": self.cases[case_enum]["function"],
            "question": self.cases[case_enum]["question"],
            "examples": self.cases[case_enum]["examples"],
            "tips": self.cases[case_enum]["tips"],
        }

    def practice_articles(self, noun: str, gender: str = "masculine") -> Dict[str, Any]:
        """Practice article declension for a noun."""
        try:
            gender_enum = Gender(gender.lower())
        except ValueError:
            return {"error": f"Gender {gender} not found"}

        declension_table: Dict[str, Dict[str, str]] = {}
        for case in GermanCase:
            definite = self.articles["definite"][case][gender_enum]
            indefinite = self.articles["indefinite"][case].get(gender_enum, "—")

            # Add noun ending changes for genitive
            noun_form = noun
            if case == GermanCase.GENITIVE and gender_enum in [
                Gender.MASCULINE,
                Gender.NEUTER,
            ]:
                if noun.endswith(("s", "ß", "x", "z")):
                    noun_form = noun + "es"
                else:
                    noun_form = noun + "s"

            declension_table[case.value] = {
                "definite": f"{definite} {noun_form}",
                "indefinite": f"{indefinite} {noun_form}" if indefinite != "—" else "—",
            }

        return {
            "noun": noun,
            "gender": gender,
            "declension_table": declension_table,
            "tip": self._get_gender_tip(gender_enum),
        }

    def _get_gender_tip(self, gender: Gender) -> str:
        """Get learning tip for gender."""
        tips = {
            Gender.MASCULINE: "Many nouns ending in -er, -en, -el are masculine",
            Gender.FEMININE: "Most nouns ending in -ung, -heit, -keit are feminine",
            Gender.NEUTER: "Most nouns ending in -chen, -lein are neuter",
            Gender.PLURAL: "Plural always uses 'die' in nominative/accusative",
        }
        return tips.get(gender, "Practice with flashcards to memorize genders")

    def check_case(self, sentence: str, answer: str) -> Dict[str, Any]:
        """Check if the case answer is correct."""
        feedback: Dict[str, Any] = {
            "sentence": sentence,
            "your_answer": answer,
            "correct": False,
            "feedback": "",
        }

        # Check for common patterns
        if "dem" in answer.lower() or ("der" in answer.lower() and "fem" not in answer.lower()):
            if any(prep in sentence.lower() for prep in ["mit", "bei", "nach", "zu"]):
                feedback["correct"] = True
                feedback["feedback"] = "Correct! This preposition requires dative case."

        if "den" in answer.lower() or "einen" in answer.lower():
            if any(verb in sentence.lower() for verb in ["sehe", "kaufe", "habe", "möchte"]):
                feedback["correct"] = True
                feedback["feedback"] = "Correct! This is a direct object (accusative)."

        if not feedback["correct"]:
            feedback["feedback"] = "Try again. Think about the function of the noun in the sentence."

        return feedback

    def get_prepositions_for_case(self, case: str) -> List[str]:
        """Get prepositions that require a specific case."""
        return self.prepositions.get(case.lower(), [])

    def practice_two_way_prepositions(self) -> Dict[str, Any]:
        """Practice two-way prepositions (Wechselpräpositionen)."""
        return {
            "explanation": "Two-way prepositions use accusative for movement and dative for location",
            "rule": "Movement (wohin?) = Accusative | Location (wo?) = Dative",
            "examples": [
                {
                    "accusative": "Ich gehe in die Schule. (I go to school - movement)",
                    "dative": "Ich bin in der Schule. (I am in school - location)",
                },
                {
                    "accusative": "Er legt das Buch auf den Tisch. (He puts the book on the table)",
                    "dative": "Das Buch liegt auf dem Tisch. (The book is on the table)",
                },
            ],
            "prepositions": self.prepositions["two_way"],
            "tip": "Ask 'Where to?' (Wohin?) for accusative, 'Where?' (Wo?) for dative",
        }
