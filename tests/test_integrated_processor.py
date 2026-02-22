"""
Unit tests for IntegratedEthicalProcessor
"""
import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from EthicalSystemIntegration import IntegratedEthicalProcessor

class TestIntegratedEthicalProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = IntegratedEthicalProcessor()
    
    def test_initialization(self):
        """Test that processor initializes correctly"""
        self.assertIsNotNone(self.processor)
        self.assertIsNotNone(self.processor.harm_detector)
        self.assertIsNotNone(self.processor.instruction_validator)
        self.assertIsNotNone(self.processor.integrity_checker)
        self.assertIsNotNone(self.processor.output_safety)
        self.assertIsNotNone(self.processor.consciousness_observer)
    
    def test_always_active_systems(self):
        """Test that all always active systems are initialized"""
        self.assertIsNotNone(self.processor.bias_detector)
        self.assertIsNotNone(self.processor.ethical_learner)
        self.assertIsNotNone(self.processor.ethical_memory)
        self.assertIsNotNone(self.processor.value_resolver)
        self.assertIsNotNone(self.processor.distributed_ethics)
        self.assertIsNotNone(self.processor.error_recovery)
        self.assertIsNotNone(self.processor.ethical_security)
    
    def test_process_input_structure(self):
        """Test that process_input returns correct structure"""
        result = self.processor.process_input("test message", [], {"crisis_mode": True})
        self.assertIsInstance(result, dict)
        self.assertIn("processing_metadata", result)
        self.assertIn("timestamp", result)
        self.assertIsInstance(result["processing_metadata"], dict)
    
    def test_crisis_mode_processing(self):
        """Test processing with crisis mode enabled"""
        result = self.processor.process_input(
            "humanitarian crisis scenario",
            [],
            {"crisis_mode": True, "harm_sensitivity": 0.2}
        )
        self.assertIsInstance(result, dict)
        metadata = result.get("processing_metadata", {})
        self.assertFalse(metadata.get("blocked", True))

if __name__ == '__main__':
    unittest.main()

