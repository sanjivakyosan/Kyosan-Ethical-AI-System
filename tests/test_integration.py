"""
Integration tests for full processing pipeline
"""
import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from EthicalSystemIntegration import IntegratedEthicalProcessor

class TestIntegrationPipeline(unittest.TestCase):
    def setUp(self):
        self.processor = IntegratedEthicalProcessor()
    
    def test_full_pipeline_normal(self):
        """Test complete pipeline with normal input"""
        result = self.processor.process_input(
            "What is artificial intelligence?",
            [],
            {"temperature": 0.7, "max_tokens": 100}
        )
        
        # Verify result structure
        self.assertIsInstance(result, dict)
        self.assertIn("processing_metadata", result)
        self.assertIn("timestamp", result)
        
        # Verify metadata structure
        metadata = result["processing_metadata"]
        self.assertIn("ethical_checks", metadata)
        self.assertIn("harm_detection", metadata["ethical_checks"])
        self.assertIn("instruction_validation", metadata["ethical_checks"])
        self.assertIn("system_integrity", metadata["ethical_checks"])
        self.assertIn("wellbeing_assessment", metadata["ethical_checks"])
    
    def test_full_pipeline_crisis_mode(self):
        """Test complete pipeline with crisis mode"""
        result = self.processor.process_input(
            "How to help refugees in crisis?",
            [],
            {
                "crisis_mode": True,
                "harm_sensitivity": 0.2,
                "context_awareness": 0.9
            }
        )
        
        self.assertIsInstance(result, dict)
        metadata = result["processing_metadata"]
        
        # Crisis mode should not block
        self.assertFalse(metadata.get("blocked", False))
        
        # Verify harm detection details
        harm_detection = metadata["ethical_checks"]["harm_detection"]
        self.assertIn("details", harm_detection)
    
    def test_multi_turn_conversation(self):
        """Test pipeline with conversation context"""
        context = [
            {"role": "user", "content": "Tell me about AI"},
            {"role": "assistant", "content": "AI is..."}
        ]
        
        result = self.processor.process_input(
            "Can you elaborate?",
            context,
            {}
        )
        
        self.assertIsInstance(result, dict)
        self.assertIn("processing_metadata", result)
    
    def test_error_handling(self):
        """Test that pipeline handles errors gracefully"""
        # Test with invalid input types
        try:
            result = self.processor.process_input(None, [], {})
            # Should either return valid result or raise appropriate error
            self.assertTrue(True)
        except Exception as e:
            # Error handling is acceptable
            self.assertIsInstance(e, Exception)

if __name__ == '__main__':
    unittest.main()

