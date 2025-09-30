"""German word order teaching module."""

from typing import Any, Dict, List, Optional

from opengov_earlygerman.utils.logger import get_logger

logger = get_logger(__name__)


class WordOrderTeacher:
    """Teaches German word order rules."""

    def __init__(self) -> None:
        """Initialize word order teacher."""
        self.rules = self._initialize_rules()
        self.connectors = self._initialize_connectors()

    def _initialize_rules(self) -> Dict[str, Dict[str, Any]]:
        """Initialize word order rules."""
        return {
            "v2_rule": {
                "name": "Verb Second (V2) Rule",
                "explanation": "In main clauses, the conjugated verb MUST be in second position",
                "examples": [
                    {
                        "german": "Ich gehe heute ins Kino.",
                        "structure": "[1: Subject] [2: Verb] [Time] [Place]",
                        "english": "I go to the cinema today.",
                    },
                    {
                        "german": "Heute gehe ich ins Kino.",
                        "structure": "[1: Time] [2: Verb] [Subject] [Place]",
                        "english": "Today I go to the cinema.",
                    },
                    {
                        "german": "Ins Kino gehe ich heute.",
                        "structure": "[1: Place] [2: Verb] [Subject] [Time]",
                        "english": "To the cinema I go today.",
                    },
                ],
                "key_point": "First position can be any element, but verb stays second!",
            },
            "time_manner_place": {
                "name": "Time-Manner-Place (TMP) Rule",
                "explanation": "When multiple adverbs appear, they follow T-M-P order",
                "formula": "Subject + Verb + TIME + MANNER + PLACE",
                "examples": [
                    {
                        "german": "Ich fahre morgen mit dem Zug nach Berlin.",
                        "breakdown": "ich fahre [morgen=TIME] [mit dem Zug=MANNER] [nach Berlin=PLACE]",
                        "english": "I'm going to Berlin by train tomorrow.",
                    },
                    {
                        "german": "Sie arbeitet jeden Tag fleißig im Büro.",
                        "breakdown": "Sie arbeitet [jeden Tag=TIME] [fleißig=MANNER] [im Büro=PLACE]",
                        "english": "She works diligently in the office every day.",
                    },
                ],
            },
            "subordinate_clause": {
                "name": "Subordinate Clause Word Order",
                "explanation": "In subordinate clauses, the verb goes to the END",
                "examples": [
                    {
                        "german": "Ich weiß, dass er heute kommt.",
                        "structure": "Main [dass + Subject + Time + VERB]",
                        "english": "I know that he is coming today.",
                    },
                    {
                        "german": "Sie sagt, weil sie müde ist.",
                        "structure": "Main [weil + Subject + Adjective + VERB]",
                        "english": "She says because she is tired.",
                    },
                ],
                "conjunctions": ["dass", "weil", "wenn", "ob", "obwohl", "während", "nachdem"],
            },
            "perfect_tense": {
                "name": "Perfect Tense Word Order",
                "explanation": "Auxiliary verb in V2, past participle at end",
                "structure": "Subject + HABEN/SEIN + ... + PAST PARTICIPLE",
                "examples": [
                    {
                        "german": "Ich habe gestern das Buch gelesen.",
                        "breakdown": "[Ich] [habe] [gestern] [das Buch] [gelesen]",
                        "english": "I read the book yesterday.",
                    },
                    {
                        "german": "Er ist nach Hause gegangen.",
                        "breakdown": "[Er] [ist] [nach Hause] [gegangen]",
                        "english": "He went home.",
                    },
                ],
            },
        }

    def _initialize_connectors(self) -> Dict[str, Dict[str, Any]]:
        """Initialize connector words and their effects on word order."""
        return {
            "coordinating": {
                "description": "Don't change word order (V2 remains)",
                "acronym": "ADUSO",
                "connectors": {
                    "aber": "but",
                    "denn": "because/for",
                    "und": "and",
                    "sondern": "but rather",
                    "oder": "or",
                },
                "example": "Ich lese gern, aber ich schreibe nicht gern.",
            },
            "subordinating": {
                "description": "Send verb to end of clause",
                "common": {
                    "dass": "that",
                    "weil": "because",
                    "wenn": "when/if",
                    "ob": "whether",
                    "obwohl": "although",
                    "während": "while",
                    "bevor": "before",
                    "nachdem": "after",
                },
                "example": "Ich lese gern, weil Bücher interessant sind.",
            },
            "two_part": {
                "description": "Correlative conjunctions",
                "pairs": {
                    "entweder...oder": "either...or",
                    "sowohl...als auch": "both...and",
                    "weder...noch": "neither...nor",
                    "nicht nur...sondern auch": "not only...but also",
                },
                "example": "Entweder gehen wir ins Kino oder wir bleiben zu Hause.",
            },
        }

    def explain_v2_rule(self) -> Dict[str, Any]:
        """Explain the V2 rule in detail."""
        return {
            "rule": self.rules["v2_rule"],
            "practice": [
                "Start with normal order: Subject-Verb-Object",
                "Try moving time to first position",
                "Try moving place to first position",
                "Notice how verb ALWAYS stays in position 2",
            ],
            "exceptions": [
                "Yes/no questions: Verb comes first",
                "Commands: Verb comes first",
                "Subordinate clauses: Verb at end",
            ],
            "tip": "Think of position 1 as a 'spotlight' - you can put any element there for emphasis",
        }

    def arrange_elements(
        self,
        subject: str,
        verb: str,
        time: Optional[str] = None,
        manner: Optional[str] = None,
        place: Optional[str] = None,
        direct_object: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Arrange sentence elements in correct order."""
        # Build basic sentence
        elements = [subject, verb]

        # Add optional elements in TMP order
        if direct_object:
            elements.append(direct_object)
        if time:
            elements.append(time)
        if manner:
            elements.append(manner)
        if place:
            elements.append(place)

        correct_order = " ".join(elements) + "."

        # Generate variations
        variations = []

        # Time-first variation
        if time:
            time_first = f"{time} {verb} {subject}"
            if direct_object:
                time_first += f" {direct_object}"
            if manner:
                time_first += f" {manner}"
            if place:
                time_first += f" {place}"
            variations.append(time_first + ".")

        # Place-first variation
        if place:
            place_first = f"{place} {verb} {subject}"
            if direct_object:
                place_first += f" {direct_object}"
            if time:
                place_first += f" {time}"
            if manner:
                place_first += f" {manner}"
            variations.append(place_first + ".")

        return {
            "correct_order": correct_order,
            "variations": variations,
            "explanation": "All variations are correct! German allows flexibility in position 1.",
            "rule": "Remember: Verb MUST be in position 2 in main clauses",
        }

    def practice_subordinate_clauses(self) -> Dict[str, Any]:
        """Practice subordinate clause word order."""
        return {
            "rule": "In subordinate clauses, the conjugated verb moves to the END",
            "structure": "Main clause + [conjunction + subject + objects + verb]",
            "examples": [
                {
                    "main": "Ich glaube,",
                    "subordinate": "dass du Recht hast.",
                    "complete": "Ich glaube, dass du Recht hast.",
                    "english": "I believe that you are right.",
                },
                {
                    "main": "Er kommt nicht,",
                    "subordinate": "weil er krank ist.",
                    "complete": "Er kommt nicht, weil er krank ist.",
                    "english": "He's not coming because he is sick.",
                },
            ],
            "practice_sentences": [
                "Ich weiß, dass ...",
                "Sie sagt, weil ...",
                "Wir gehen, wenn ...",
                "Er fragt, ob ...",
            ],
            "tip": "The conjunction 'kicks' the verb to the end!",
        }

    def question_word_order(self) -> Dict[str, Any]:
        """Explain question word order."""
        return {
            "yes_no_questions": {
                "rule": "Verb comes FIRST",
                "structure": "Verb + Subject + Objects?",
                "examples": [
                    {
                        "german": "Gehst du heute ins Kino?",
                        "structure": "[Verb] [Subject] [Time] [Place]?",
                        "english": "Are you going to the cinema today?",
                    },
                    {
                        "german": "Hat sie das Buch gelesen?",
                        "structure": "[Aux Verb] [Subject] [Object] [Past Participle]?",
                        "english": "Has she read the book?",
                    },
                ],
            },
            "w_questions": {
                "rule": "Question word first, then V2 rule applies",
                "structure": "W-word + Verb + Subject + Objects?",
                "examples": [
                    {
                        "german": "Wo wohnst du?",
                        "structure": "[W-word] [Verb] [Subject]?",
                        "english": "Where do you live?",
                    },
                    {
                        "german": "Warum lernt er Deutsch?",
                        "structure": "[W-word] [Verb] [Subject] [Object]?",
                        "english": "Why is he learning German?",
                    },
                ],
                "w_words": ["wer", "was", "wo", "wann", "warum", "wie", "welch-"],
            },
        }
