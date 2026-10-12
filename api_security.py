"""
Request limits and conversation path checks for the Flask API.
"""
import os
import re
from typing import Optional

CONVERSATION_ID_PATTERN = re.compile(r'^conv_[0-9]{1,20}$')

DEFAULT_MAX_TOKENS = 4096
MAX_TOKENS_CAP = 8192
MAX_REQUEST_BYTES = 1_048_576


def clamp_max_tokens(value, default: int = DEFAULT_MAX_TOKENS, cap: int = MAX_TOKENS_CAP) -> int:
    """Clamp requested completion length to a safe server maximum."""
    try:
        tokens = int(value)
    except (TypeError, ValueError):
        return default
    if tokens < 1:
        return default
    return min(tokens, cap)


def conversation_file_path(conversations_dir: str, conversation_id: str) -> Optional[str]:
    """
    Return a real path under conversations_dir for a generated id, or None if unsafe.
    """
    if not conversation_id or not CONVERSATION_ID_PATTERN.fullmatch(conversation_id):
        return None
    base = os.path.realpath(conversations_dir)
    candidate = os.path.realpath(os.path.join(base, f'{conversation_id}.json'))
    if os.path.dirname(candidate) != base:
        return None
    return candidate
