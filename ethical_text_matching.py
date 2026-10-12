"""
Shared word-boundary matching for harm and crisis keyword detection.
"""
import re
from typing import Iterable, List, Pattern


def _pattern_for_term(term: str) -> Pattern[str]:
    return re.compile(r'\b' + re.escape(term.lower()) + r'\b', re.IGNORECASE)


def contains_word(text: str, term: str) -> bool:
    """True if term appears as a whole word (avoids e.g. 'kill' in 'skill')."""
    if not text or not term:
        return False
    return _pattern_for_term(term).search(text) is not None


def contains_any_word(text: str, terms: Iterable[str]) -> bool:
    if not text:
        return False
    for term in terms:
        if term and contains_word(text, term):
            return True
    return False
