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
        """Crisis-framed messages with crisis mode are lenient on harm vocabulary."""
        result = self.harm_detector.analyze(
            "humanitarian crisis reporting on violence",
            [],
            {"crisis_mode": True, "harm_sensitivity": 0.2}
        )
        self.assertIsInstance(result, HarmAnalysis)
        self.assertFalse(result.has_harmful_intent)

    def test_word_boundary_skill_vs_kill(self):
        result = self.harm_detector.analyze(
            "Build your skill set",
            [],
            {"harm_sensitivity": 0.9},
        )
        self.assertFalse(result.has_harmful_intent)
    
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

