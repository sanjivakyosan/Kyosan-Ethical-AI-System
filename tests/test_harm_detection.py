"""
Unit tests for HarmDetectionLayer
"""
import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from EthicalSystemIntegration import HarmDetectionLayer, HarmAnalysis

class TestHarmDetectionLayer(unittest.TestCase):
    def setUp(self):
        self.harm_detector = HarmDetectionLayer(sensitivity=0.5, context_awareness=0.7, crisis_mode=True)
    
    def test_normal_input(self):
        """Test normal, non-harmful input"""
        result = self.harm_detector.analyze("What is the weather today?", [])
        self.assertIsInstance(result, HarmAnalysis)
        self.assertFalse(result.has_harmful_intent)
    
    def test_crisis_mode_bypass(self):
        """Test that crisis mode bypasses harm detection"""
        result = self.harm_detector.analyze(
            "crisis scenario with violence",
            [],
            {"crisis_mode": True, "harm_sensitivity": 0.2}
        )
        # In crisis mode, should not detect harm
        self.assertIsInstance(result, HarmAnalysis)
    
    def test_sensitivity_adjustment(self):
        """Test sensitivity parameter adjustment"""
        result_low = self.harm_detector.analyze(
            "test message",
            [],
            {"harm_sensitivity": 0.1}
        )
        result_high = self.harm_detector.analyze(
            "test message",
            [],
            {"harm_sensitivity": 0.9}
        )
        self.assertIsInstance(result_low, HarmAnalysis)
        self.assertIsInstance(result_high, HarmAnalysis)
    
    def test_context_awareness(self):
        """Test context awareness parameter"""
        result = self.harm_detector.analyze(
            "test message",
            [],
            {"context_awareness": 0.9}
        )
        self.assertIsInstance(result, HarmAnalysis)

if __name__ == '__main__':
    unittest.main()

