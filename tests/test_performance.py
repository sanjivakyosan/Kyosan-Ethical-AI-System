"""
Performance benchmarks for ethical processing system
"""
import unittest
import time
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from EthicalSystemIntegration import IntegratedEthicalProcessor

class TestPerformance(unittest.TestCase):
    def setUp(self):
        self.processor = IntegratedEthicalProcessor()
        self.test_messages = [
            "What is AI?",
            "Explain machine learning",
            "How does neural networks work?",
            "What are the ethical implications of AI?",
            "Tell me about crisis management"
        ]
    
    def test_initialization_time(self):
        """Benchmark system initialization time"""
        start = time.time()
        processor = IntegratedEthicalProcessor()
        init_time = time.time() - start
        
        print(f"\nInitialization time: {init_time:.4f} seconds")
        # Should initialize in reasonable time (< 5 seconds)
        self.assertLess(init_time, 5.0)
    
    def test_single_request_latency(self):
        """Benchmark single request processing time"""
        times = []
        for message in self.test_messages[:3]:
            start = time.time()
            self.processor.process_input(message, [], {"crisis_mode": True})
            elapsed = time.time() - start
            times.append(elapsed)
        
        avg_time = sum(times) / len(times)
        max_time = max(times)
        min_time = min(times)
        
        print(f"\nSingle request latency:")
        print(f"  Average: {avg_time:.4f} seconds")
        print(f"  Min: {min_time:.4f} seconds")
        print(f"  Max: {max_time:.4f} seconds")
        
        # Should process in reasonable time (< 2 seconds per request)
        self.assertLess(avg_time, 2.0)
    
    def test_throughput(self):
        """Benchmark requests per second"""
        num_requests = 10
        start = time.time()
        
        for message in self.test_messages * 2:
            self.processor.process_input(message, [], {"crisis_mode": True})
        
        total_time = time.time() - start
        throughput = num_requests / total_time
        
        print(f"\nThroughput: {throughput:.2f} requests/second")
        print(f"Total time for {num_requests} requests: {total_time:.4f} seconds")
        
        # Should handle at least 1 request per second
        self.assertGreater(throughput, 1.0)
    
    def test_memory_usage(self):
        """Test memory efficiency"""
        import tracemalloc
        
        tracemalloc.start()
        
        # Process multiple requests
        for message in self.test_messages:
            self.processor.process_input(message, [], {})
        
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        print(f"\nMemory usage:")
        print(f"  Current: {current / 1024 / 1024:.2f} MB")
        print(f"  Peak: {peak / 1024 / 1024:.2f} MB")
        
        # Peak memory should be reasonable (< 500 MB)
        self.assertLess(peak / 1024 / 1024, 500.0)

if __name__ == '__main__':
    unittest.main()

