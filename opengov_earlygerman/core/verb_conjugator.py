"""German verb conjugation system."""

from typing import Any, Dict, List

from opengov_earlygerman.core.models import CEFRLevel, Verb, VerbType
from opengov_earlygerman.utils.logger import get_logger

logger = get_logger(__name__)


class VerbConjugator:
    """German verb conjugation engine."""

    def __init__(self) -> None:
        """Initialize verb conjugator."""
        self.weak_endings = self._load_weak_endings()
        self.strong_verbs = self._load_strong_verbs()
        self.modal_verbs = self._load_modal_verbs()
        self.separable_prefixes = self._load_separable_prefixes()

    def _load_weak_endings(self) -> Dict[str, Dict[str, str]]:
        """Load weak (regular) verb endings."""
        return {
            "present": {
                "ich": "e",
                "du": "st",
                "er/sie/es": "t",
                "wir": "en",
                "ihr": "t",
                "sie/Sie": "en",
            },
            "preterite": {
                "ich": "te",
                "du": "test",
                "er/sie/es": "te",
                "wir": "ten",
                "ihr": "tet",
                "sie/Sie": "ten",
            },
            "perfect_participle": "ge-{stem}-t",
        }

    def _load_strong_verbs(self) -> Dict[str, Verb]:
        """Load strong (irregular) verb database."""
        strong_verbs = {}

        # Sein (to be)
        strong_verbs["sein"] = Verb(
            id="verb_sein",
            infinitive="sein",
            english="to be",
            verb_type=VerbType.STRONG,
            conjugations={
                "present": {
                    "ich": "bin",
                    "du": "bist",
                    "er/sie/es": "ist",
                    "wir": "sind",
                    "ihr": "seid",
                    "sie/Sie": "sind",
                },
                "preterite": {
                    "ich": "war",
                    "du": "warst",
                    "er/sie/es": "war",
                    "wir": "waren",
                    "ihr": "wart",
                    "sie/Sie": "waren",
                },
            },
            partizip_2="gewesen",
            auxiliary_verb="sein",
            level=CEFRLevel.A1,
        )

        # Haben (to have)
        strong_verbs["haben"] = Verb(
            id="verb_haben",
            infinitive="haben",
            english="to have",
            verb_type=VerbType.STRONG,
            conjugations={
                "present": {
                    "ich": "habe",
                    "du": "hast",
                    "er/sie/es": "hat",
                    "wir": "haben",
                    "ihr": "habt",
                    "sie/Sie": "haben",
                },
                "preterite": {
                    "ich": "hatte",
                    "du": "hattest",
                    "er/sie/es": "hatte",
                    "wir": "hatten",
                    "ihr": "hattet",
                    "sie/Sie": "hatten",
                },
            },
            partizip_2="gehabt",
            auxiliary_verb="haben",
            level=CEFRLevel.A1,
        )

        # Werden (to become)
        strong_verbs["werden"] = Verb(
            id="verb_werden",
            infinitive="werden",
            english="to become",
            verb_type=VerbType.STRONG,
            conjugations={
                "present": {
                    "ich": "werde",
                    "du": "wirst",
                    "er/sie/es": "wird",
                    "wir": "werden",
                    "ihr": "werdet",
                    "sie/Sie": "werden",
                },
            },
            partizip_2="geworden",
            auxiliary_verb="sein",
            level=CEFRLevel.A1,
        )

        return strong_verbs

    def _load_modal_verbs(self) -> Dict[str, Dict[str, Dict[str, str]]]:
        """Load modal verb conjugations."""
        return {
            "können": {
                "present": {
                    "ich": "kann",
                    "du": "kannst",
                    "er/sie/es": "kann",
                    "wir": "können",
                    "ihr": "könnt",
                    "sie/Sie": "können",
                },
            },
            "müssen": {
                "present": {
                    "ich": "muss",
                    "du": "musst",
                    "er/sie/es": "muss",
                    "wir": "müssen",
                    "ihr": "müsst",
                    "sie/Sie": "müssen",
                },
            },
            "wollen": {
                "present": {
                    "ich": "will",
                    "du": "willst",
                    "er/sie/es": "will",
                    "wir": "wollen",
                    "ihr": "wollt",
                    "sie/Sie": "wollen",
                },
            },
            "sollen": {
                "present": {
                    "ich": "soll",
                    "du": "sollst",
                    "er/sie/es": "soll",
                    "wir": "sollen",
                    "ihr": "sollt",
                    "sie/Sie": "sollen",
                },
            },
            "dürfen": {
                "present": {
                    "ich": "darf",
                    "du": "darfst",
                    "er/sie/es": "darf",
                    "wir": "dürfen",
                    "ihr": "dürft",
                    "sie/Sie": "dürfen",
                },
            },
            "mögen": {
                "present": {
                    "ich": "mag",
                    "du": "magst",
                    "er/sie/es": "mag",
                    "wir": "mögen",
                    "ihr": "mögt",
                    "sie/Sie": "mögen",
                },
            },
        }

    def _load_separable_prefixes(self) -> List[str]:
        """Load common separable prefixes."""
        return [
            "ab",
            "an",
            "auf",
            "aus",
            "bei",
            "ein",
            "los",
            "mit",
            "nach",
            "her",
            "hin",
            "vor",
            "weg",
            "zu",
            "zurück",
            "zusammen",
            "weiter",
        ]

    def conjugate(
        self, infinitive: str, tense: str = "present", include_formal: bool = True
    ) -> Dict[str, Any]:
        """Conjugate a German verb."""
        # Check if it's a strong/irregular verb
        if infinitive in self.strong_verbs:
            verb = self.strong_verbs[infinitive]
            if tense in verb.conjugations:
                return {
                    "infinitive": infinitive,
                    "tense": tense,
                    "forms": verb.conjugations[tense],
                    "type": "strong",
                    "auxiliary": verb.auxiliary_verb,
                    "participle": verb.partizip_2,
                }

        # Check if it's a modal verb
        if infinitive in self.modal_verbs:
            if tense in self.modal_verbs[infinitive]:
                return {
                    "infinitive": infinitive,
                    "tense": tense,
                    "forms": self.modal_verbs[infinitive][tense],
                    "type": "modal",
                }

        # Regular (weak) verb conjugation
        stem = self._get_stem(infinitive)
        endings = self.weak_endings.get(tense, {})

        forms = {}
        for pronoun, ending in endings.items():
            # Handle stem changes for certain letters
            if stem.endswith(("t", "d", "n")) and ending.startswith(("st", "t")):
                forms[pronoun] = stem + "e" + ending
            else:
                forms[pronoun] = stem + ending

        return {
            "infinitive": infinitive,
            "tense": tense,
            "forms": forms,
            "type": "weak",
            "auxiliary": "haben",
            "participle": f"ge{stem}t",
        }

    def _get_stem(self, infinitive: str) -> str:
        """Get verb stem from infinitive."""
        if infinitive.endswith("en"):
            return infinitive[:-2]
        elif infinitive.endswith("n"):
            return infinitive[:-1]
        return infinitive

    def handle_separable(self, verb: str, sentence_type: str = "main_clause") -> Dict[str, Any]:
        """Handle separable verb conjugation and placement."""
        # Check if verb has separable prefix
        prefix = None
        base_verb = verb
        for sep_prefix in self.separable_prefixes:
            if verb.startswith(sep_prefix):
                prefix = sep_prefix
                base_verb = verb[len(prefix) :]
                break

        if not prefix:
            return {"error": "Not a separable verb"}

        # Conjugate base verb
        conjugated = self.conjugate(base_verb)

        examples = []
        if sentence_type == "main_clause":
            examples = [
                {
                    "structure": f"Subject + {conjugated['forms']['er/sie/es']} + ... + {prefix}",
                    "example": f"Er {conjugated['forms']['er/sie/es']} um 7 Uhr {prefix}.",
                    "english": "He gets up at 7 o'clock.",
                },
            ]
        else:
            examples = [
                {
                    "structure": f"..., weil + Subject + ... + {prefix}{conjugated['forms']['er/sie/es']}",
                    "example": f"..., weil er um 7 Uhr {prefix}{conjugated['forms']['er/sie/es']}.",
                    "english": "..., because he gets up at 7 o'clock.",
                },
            ]

        return {
            "verb": verb,
            "prefix": prefix,
            "base_verb": base_verb,
            "sentence_type": sentence_type,
            "examples": examples,
            "rule": "In main clauses, prefix goes to end. In subordinate clauses, verb stays together.",
        }

    def with_modal(self, modal: str, main_verb: str) -> Dict[str, Any]:
        """Combine modal verb with main verb."""
        modal_conj = self.conjugate(modal)

        return {
            "structure": "Modal verb (conjugated) + ... + main verb (infinitive)",
            "modal": modal,
            "main_verb": main_verb,
            "conjugation": modal_conj["forms"],
            "examples": [
                {
                    "german": f"Ich {modal_conj['forms']['ich']} {main_verb}.",
                    "english": f"I {self._translate_modal(modal)} {main_verb}.",
                },
                {
                    "german": f"Sie {modal_conj['forms']['sie/Sie']} das nicht {main_verb}.",
                    "english": f"They {self._translate_modal(modal)} not {main_verb} that.",
                },
            ],
            "rule": "Modal verb conjugated in V2 position, main verb as infinitive at end",
        }

    def _translate_modal(self, modal: str) -> str:
        """Translate modal verb to English."""
        translations = {
            "können": "can",
            "müssen": "must",
            "wollen": "want to",
            "sollen": "should",
            "dürfen": "may",
            "mögen": "like to",
        }
        return translations.get(modal, modal)
