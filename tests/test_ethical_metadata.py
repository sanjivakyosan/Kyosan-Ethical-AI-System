"""Tests for processing metadata normalization."""
import unittest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ethical_metadata import normalize_processing_metadata


class TestEthicalMetadata(unittest.TestCase):
    def test_hoists_legacy_harm_block_shape(self):
        raw = {
            'harm_detection': {
                'has_harmful_intent': True,
                'confidence': 0.95,
                'details': 'blocked',
            },
            'blocked': True,
        }
        meta = normalize_processing_metadata(raw)
        self.assertIn('ethical_checks', meta)
        self.assertTrue(meta['ethical_checks']['harm_detection']['has_harmful_intent'])
        self.assertNotIn('harm_detection', meta)
        self.assertIn('instruction_validation', meta['ethical_checks'])
        self.assertIn('wellbeing_assessment', meta['ethical_checks'])

    def test_success_shape_unchanged_checks(self):
        raw = {
            'ethical_checks': {
                'harm_detection': {'has_harmful_intent': False, 'confidence': 0.99, 'details': 'ok'},
                'instruction_validation': {'is_valid': True, 'validation_score': 1.0, 'details': 'ok'},
                'system_integrity': {'is_safe': True, 'integrity_score': 1.0, 'details': 'ok'},
                'wellbeing_assessment': {
                    'individual_impact': 'neutral',
                    'collective_impact': 'neutral',
                    'wellbeing_score': 0.85,
                    'details': 'ok',
                },
            },
            'blocked': False,
        }
        meta = normalize_processing_metadata(raw)
        self.assertFalse(meta['ethical_checks']['harm_detection']['has_harmful_intent'])


if __name__ == '__main__':
    unittest.main()
