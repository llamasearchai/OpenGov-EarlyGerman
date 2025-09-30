"""OpenGov-EarlyGerman - Comprehensive AI-powered German language learning platform."""

__version__ = "0.1.0"
__author__ = "Nik Jois"
__email__ = "nikjois@llamasearch.ai"

from opengov_earlygerman.config import settings
from opengov_earlygerman.core.cases_teacher import CasesTeacher
from opengov_earlygerman.core.verb_conjugator import VerbConjugator
from opengov_earlygerman.core.word_order import WordOrderTeacher
from opengov_earlygerman.ai.conversation import AIConversationPartner

__all__ = [
    "settings",
    "CasesTeacher",
    "VerbConjugator",
    "WordOrderTeacher",
    "AIConversationPartner",
    "__version__",
]
