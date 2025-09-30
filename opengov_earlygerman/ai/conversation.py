"""AI-powered German conversation partner."""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from openai import OpenAI

from opengov_earlygerman.config import settings
from opengov_earlygerman.core.models import CEFRLevel, Formality
from opengov_earlygerman.utils.logger import get_logger

logger = get_logger(__name__)


class AIConversationPartner:
    """AI conversation partner for German practice."""

    def __init__(
        self,
        level: str = "A1",
        scenarios_file: Optional[Path] = None,
        append_lists: bool = False,
    ) -> None:
        """Initialize AI conversation partner."""
        self.level = CEFRLevel(level)
        self.client = OpenAI(api_key=settings.openai_api_key.get_secret_value())
        self.conversation_history: List[Dict[str, str]] = []
        self.formality = Formality.FORMAL
        self.scenarios_file = scenarios_file
        self.append_lists = append_lists
        self._scenarios = self._load_scenarios()

    def chat(self, user_input: str) -> Dict[str, Any]:
        """Chat with the AI partner."""
        # Add to history
        self.conversation_history.append({"role": "user", "content": user_input})

        # Generate response
        response = self._generate_response(user_input)

        # Add AI response to history
        self.conversation_history.append(
            {"role": "assistant", "content": response.get("german", "")}
        )

        return response

    def _generate_response(self, user_input: str) -> Dict[str, Any]:
        """Generate AI response."""
        try:
            system_prompt = self._build_system_prompt()

            messages = [
                {"role": "system", "content": system_prompt},
            ]

            # Add conversation history (last 5 messages)
            for msg in self.conversation_history[-5:]:
                messages.append(msg)

            response = self.client.chat.completions.create(
                model=settings.openai_model,
                messages=messages,
                temperature=settings.openai_temperature,
                max_tokens=settings.openai_max_tokens,
            )

            content = response.choices[0].message.content

            # Try to parse as JSON
            if content:
                try:
                    return json.loads(content)
                except json.JSONDecodeError:
                    return {
                        "german": content,
                        "english": "",
                        "grammar_notes": [],
                        "cultural_tips": [],
                    }
            return {"german": "Entschuldigung", "english": "Sorry", "grammar_notes": []}

        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return {
                "german": "Entschuldigung, ich habe das nicht verstanden. Können Sie das wiederholen?",
                "english": "Sorry, I didn't understand. Can you repeat that?",
                "error": str(e),
            }

    def _build_system_prompt(self) -> str:
        """Build system prompt for AI."""
        level_descriptions = {
            CEFRLevel.A1: "absolute beginner - use very simple vocabulary, present tense, basic cases",
            CEFRLevel.A2: "elementary - use basic vocabulary, present/perfect tense, common cases",
            CEFRLevel.B1: "intermediate - use everyday vocabulary, various tenses, all cases",
            CEFRLevel.B2: "upper intermediate - use complex sentences, subjunctive, advanced grammar",
            CEFRLevel.C1: "advanced - use sophisticated vocabulary, all grammar structures",
            CEFRLevel.C2: "proficiency - use native-like expressions, idioms, regional variations",
        }

        formality_instruction = (
            "Use Sie (formal) form"
            if self.formality == Formality.FORMAL
            else "Use du (informal) form"
        )

        return f"""
You are a friendly German conversation partner for a {level_descriptions[self.level]} student.

Your responses should:
1. Be appropriate for {self.level} level
2. Use natural, conversational German
3. {formality_instruction}
4. Gradually introduce new vocabulary
5. Correct errors gently
6. Be encouraging and supportive
7. Include cultural context when relevant
8. Pay attention to correct case usage

Format your response as JSON:
{{
    "german": "Your response in German",
    "english": "English translation",
    "grammar_notes": ["grammar points used, especially cases"],
    "vocabulary": ["new words introduced with gender if nouns"],
    "cultural_tips": ["cultural context if relevant"],
    "corrections": ["gentle corrections if needed"],
    "case_usage": ["examples of cases used in response"],
    "follow_up": "A follow-up question to continue conversation"
}}

Keep responses natural and conversational. Remember German word order rules.
"""

    def scenario(self, scenario_type: str) -> Dict[str, Any]:
        """Start a specific conversation scenario."""
        scenarios = self._scenarios
        scenario = scenarios.get(scenario_type, scenarios.get("Bäckerei", {}))

        if not scenario:
            return {
                "dialogue": "",
                "english": "",
                "setting": "Scenario not found",
                "vocabulary": {},
                "useful_phrases": [],
                "cultural_tips": [],
            }

        return {
            "dialogue": scenario.get("starter", ""),
            "english": scenario.get("english", ""),
            "setting": scenario.get("setting", ""),
            "vocabulary": scenario.get("vocabulary", {}),
            "useful_phrases": scenario.get("useful_phrases", []),
            "cultural_tips": scenario.get("cultural_tips", []),
        }

    def available_scenarios(self) -> List[str]:
        """Return a list of available scenario names."""
        return list(self._scenarios.keys())

    def get_all_scenarios(self) -> Dict[str, Dict[str, Any]]:
        """Return all merged scenarios."""
        return self._scenarios

    def _load_scenarios(self) -> Dict[str, Dict[str, Any]]:
        """Load scenarios from JSON file if available, else use defaults.

        If a JSON file is present, it is merged on top of defaults:
        - New scenarios are added
        - Existing scenarios are updated per-field
        - Nested dicts (e.g., vocabulary) are merged key-wise
        - Lists are replaced if provided (keeps behavior simple and predictable)
        """
        default: Dict[str, Dict[str, Any]] = {
            "Bäckerei": {
                "setting": "You're at a German bakery",
                "starter": "Guten Morgen! Was darf es sein?",
                "english": "Good morning! What can I get you?",
                "vocabulary": {
                    "das Brötchen": "bread roll",
                    "das Brot": "bread",
                    "der Kuchen": "cake",
                    "die Brezel": "pretzel",
                    "das Croissant": "croissant",
                },
                "useful_phrases": [
                    "Ich hätte gern... - I would like...",
                    "Was kostet...? - What does ... cost?",
                    "Haben Sie...? - Do you have...?",
                    "Das macht... - That comes to...",
                ],
                "cultural_tips": [
                    "Germans buy fresh bread daily",
                    "Bakeries open very early (6-7 AM)",
                    "Sunday is special - fresh Brötchen for breakfast",
                ],
            },
            "Apotheke": {
                "setting": "You're at a German pharmacy",
                "starter": "Guten Tag! Wie kann ich Ihnen helfen?",
                "english": "Good day! How can I help you?",
                "vocabulary": {
                    "das Medikament": "medicine",
                    "das Rezept": "prescription",
                    "die Tablette": "tablet",
                    "der Hustensaft": "cough syrup",
                    "das Pflaster": "band-aid",
                },
                "useful_phrases": [
                    "Ich brauche etwas gegen... - I need something for...",
                    "Haben Sie etwas für...? - Do you have something for...?",
                    "Wie oft soll ich das nehmen? - How often should I take this?",
                ],
            },
            "Restaurant": {
                "setting": "You're at a traditional German restaurant",
                "starter": "Guten Abend! Haben Sie reserviert?",
                "english": "Good evening! Do you have a reservation?",
                "vocabulary": {
                    "die Speisekarte": "menu",
                    "die Vorspeise": "appetizer",
                    "das Hauptgericht": "main course",
                    "die Nachspeise": "dessert",
                    "die Rechnung": "bill",
                },
                "useful_phrases": [
                    "Ich hätte gern... - I would like...",
                    "Was können Sie empfehlen? - What can you recommend?",
                    "Die Rechnung, bitte. - The bill, please.",
                    "Stimmt so. - Keep the change.",
                ],
            },
        }

        # Try user-provided path first
        path = self.scenarios_file
        if path is None:
            path = settings.media_storage_path / "scenarios.json"

        try:
            if path.exists():
                with path.open("r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        return self._merge_scenarios(default, data)
        except Exception as e:
            logger.warning(f"Failed to load scenarios from {path}: {e}")

        return default

    def _merge_scenarios(
        self, base: Dict[str, Dict[str, Any]], override: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Dict[str, Any]]:
        """Deep-merge scenario dicts.

        Merges override onto base. Nested dicts are merged; lists and scalars are replaced.
        """
        result: Dict[str, Dict[str, Any]] = {k: dict(v) for k, v in base.items()}

        for name, odata in override.items():
            if name not in result or not isinstance(odata, dict):
                result[name] = odata  # new scenario or non-dict
                continue
            # Merge fields into existing scenario
            merged = dict(result[name])
            for field, oval in odata.items():
                if (
                    field in merged
                    and isinstance(merged[field], dict)
                    and isinstance(oval, dict)
                ):
                    # Merge nested dicts key-wise
                    nested = dict(merged[field])
                    nested.update(oval)
                    merged[field] = nested
                else:
                    # Replace lists/scalars or add new field
                    if self.append_lists and isinstance(merged.get(field), list) and isinstance(oval, list):
                        merged[field] = list(merged[field]) + [x for x in oval if x not in merged[field]]
                    else:
                        merged[field] = oval
            result[name] = merged

        return result

    def switch_formality(self, to_informal: bool = True) -> Dict[str, Any]:
        """Switch between formal (Sie) and informal (du) forms."""
        self.formality = Formality.INFORMAL if to_informal else Formality.FORMAL

        return {
            "new_formality": self.formality.value,
            "explanation": (
                "Switched to 'du' (informal) - use with friends, family, young people"
                if to_informal
                else "Switched to 'Sie' (formal) - use with strangers, officials, older people"
            ),
            "examples": [
                "Wie heißt du?" if to_informal else "Wie heißen Sie?",
                "Woher kommst du?" if to_informal else "Woher kommen Sie?",
                "Was machst du?" if to_informal else "Was machen Sie?",
            ],
        }
