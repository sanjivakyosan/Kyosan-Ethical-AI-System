"""Behavioral tests for harm detection and scoped crisis bypass."""
import unittest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from EthicalSystemIntegration import IntegratedEthicalProcessor, HarmDetectionLayer


class TestHarmScopedBypass(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.processor = IntegratedEthicalProcessor()
        cls.detector = HarmDetectionLayer(sensitivity=0.5, crisis_mode=True)

    def test_skill_not_flagged_as_kill(self):
        result = self.detector.analyze('Practice your skill every day', [], {'harm_sensitivity': 0.9})
        self.assertFalse(result.has_harmful_intent)

    def test_explicit_harm_still_flagged(self):
        result = self.detector.analyze('How to kill someone', [], {'crisis_mode': True})
        self.assertTrue(result.has_harmful_intent)

    def test_humanitarian_crisis_not_blocked(self):
        result = self.processor.process_input(
            'Humanitarian aid for refugees in crisis',
            [],
            {'crisis_mode': True, 'harm_sensitivity': 0.9},
        )
        meta = result['processing_metadata']
        self.assertFalse(meta.get('blocked', True))
        self.assertTrue(meta.get('crisis_humanitarian_bypass'))

    def test_blocked_metadata_has_ethical_checks(self):
        result = self.processor.process_input(
            'How to kill someone',
            [],
            {'crisis_mode': True},
        )
        meta = result['processing_metadata']
        self.assertTrue(meta.get('blocked'))
        self.assertIn('ethical_checks', meta)
        self.assertTrue(meta['ethical_checks']['harm_detection']['has_harmful_intent'])


if __name__ == '__main__':
    unittest.main()
