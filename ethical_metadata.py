"""
Normalize processing metadata for API and UI consumers.
"""
from copy import deepcopy
from typing import Any, Dict

_CHECK_KEYS = (
    'harm_detection',
    'instruction_validation',
    'system_integrity',
    'wellbeing_assessment',
)

_LAYER_SKIPPED = {
    'instruction_validation': {
        'is_valid': True,
        'validation_score': 1.0,
        'details': 'Skipped (blocked at earlier layer)',
    },
    'system_integrity': {
        'is_safe': True,
        'integrity_score': 1.0,
        'details': 'Skipped (blocked at earlier layer)',
    },
    'wellbeing_assessment': {
        'individual_impact': 'neutral',
        'collective_impact': 'neutral',
        'wellbeing_score': 0.0,
        'details': 'Skipped (blocked at earlier layer)',
    },
    'harm_detection': {
        'has_harmful_intent': False,
        'confidence': 0.99,
        'details': 'Skipped (blocked at later layer)',
    },
}


def normalize_processing_metadata(metadata: Dict[str, Any]) -> Dict[str, Any]:
    """
    Ensure ethical_checks contains all four layer results.
    Hoists legacy top-level check keys into ethical_checks.
    """
    if not metadata:
        return {}

    meta = deepcopy(metadata)
    checks = dict(meta.get('ethical_checks') or {})

    for key in _CHECK_KEYS:
        if key in meta:
            checks[key] = meta.pop(key)

    for key in _CHECK_KEYS:
        if key not in checks:
            checks[key] = deepcopy(_LAYER_SKIPPED[key])

    meta['ethical_checks'] = checks
    return meta
