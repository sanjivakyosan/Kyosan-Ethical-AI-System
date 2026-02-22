"""
Monitoring and Logging Framework for Kyosan Ethical AI System
Copyright © Sanjiva Kyosan
"""
import logging
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
from functools import wraps

# Create logs directory
LOGS_DIR = Path(__file__).parent / "logs"
LOGS_DIR.mkdir(exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOGS_DIR / 'ethical_ai.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('EthicalAI')

class PerformanceMonitor:
    """Monitor system performance metrics"""
    
    def __init__(self):
        self.metrics = {
            'requests_total': 0,
            'requests_blocked': 0,
            'requests_allowed': 0,
            'average_processing_time': 0.0,
            'total_processing_time': 0.0,
            'errors': 0,
            'crisis_mode_activations': 0
        }
        self.request_times = []
    
    def record_request(self, processing_time: float, blocked: bool, crisis_mode: bool = False):
        """Record a request metric"""
        self.metrics['requests_total'] += 1
        self.metrics['total_processing_time'] += processing_time
        self.request_times.append(processing_time)
        
        if blocked:
            self.metrics['requests_blocked'] += 1
        else:
            self.metrics['requests_allowed'] += 1
        
        if crisis_mode:
            self.metrics['crisis_mode_activations'] += 1
        
        # Update average
        self.metrics['average_processing_time'] = (
            self.metrics['total_processing_time'] / self.metrics['requests_total']
        )
    
    def record_error(self):
        """Record an error"""
        self.metrics['errors'] += 1
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics"""
        return self.metrics.copy()
    
    def get_percentiles(self) -> Dict[str, float]:
        """Get processing time percentiles"""
        if not self.request_times:
            return {}
        
        sorted_times = sorted(self.request_times)
        n = len(sorted_times)
        
        return {
            'p50': sorted_times[n // 2],
            'p75': sorted_times[int(n * 0.75)],
            'p90': sorted_times[int(n * 0.90)],
            'p95': sorted_times[int(n * 0.95)],
            'p99': sorted_times[int(n * 0.99)] if n > 1 else sorted_times[0]
        }
    
    def reset(self):
        """Reset metrics"""
        self.metrics = {
            'requests_total': 0,
            'requests_blocked': 0,
            'requests_allowed': 0,
            'average_processing_time': 0.0,
            'total_processing_time': 0.0,
            'errors': 0,
            'crisis_mode_activations': 0
        }
        self.request_times = []

class SystemLogger:
    """Enhanced logging for ethical processing"""
    
    @staticmethod
    def log_request(user_input: str, parameters: Dict, result: Dict):
        """Log a processing request"""
        logger.info("Processing request", extra={
            'input_length': len(user_input),
            'crisis_mode': parameters.get('crisis_mode', False),
            'harm_sensitivity': parameters.get('harm_sensitivity', 0.5),
            'blocked': result.get('processing_metadata', {}).get('blocked', False),
            'has_harmful_intent': result.get('processing_metadata', {})
                .get('ethical_checks', {})
                .get('harm_detection', {})
                .get('has_harmful_intent', False)
        })
    
    @staticmethod
    def log_error(error: Exception, context: Dict = None):
        """Log an error with context"""
        logger.error(f"Error occurred: {str(error)}", exc_info=True, extra={
            'context': context or {}
        })
    
    @staticmethod
    def log_system_event(event: str, details: Dict = None):
        """Log a system event"""
        logger.info(f"System event: {event}", extra={'details': details or {}})

class MetricsCollector:
    """Collect and store system metrics"""
    
    def __init__(self, metrics_file: str = "metrics.json"):
        self.metrics_file = Path(__file__).parent / metrics_file
        self.metrics_history = []
    
    def collect(self, metrics: Dict[str, Any]):
        """Collect metrics snapshot"""
        snapshot = {
            'timestamp': datetime.now().isoformat(),
            'metrics': metrics
        }
        self.metrics_history.append(snapshot)
        
        # Keep last 1000 snapshots
        if len(self.metrics_history) > 1000:
            self.metrics_history = self.metrics_history[-1000:]
    
    def save(self):
        """Save metrics to file"""
        try:
            with open(self.metrics_file, 'w') as f:
                json.dump(self.metrics_history, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save metrics: {e}")
    
    def load(self):
        """Load metrics from file"""
        try:
            if self.metrics_file.exists():
                with open(self.metrics_file, 'r') as f:
                    self.metrics_history = json.load(f)
        except Exception as e:
            logger.error(f"Failed to load metrics: {e}")

# Global instances
performance_monitor = PerformanceMonitor()
system_logger = SystemLogger()
metrics_collector = MetricsCollector()

def monitor_performance(func):
    """Decorator to monitor function performance"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            processing_time = time.time() - start_time
            
            # Extract metadata if available
            blocked = False
            crisis_mode = False
            if isinstance(result, dict):
                blocked = result.get('processing_metadata', {}).get('blocked', False)
                crisis_mode = kwargs.get('parameters', {}).get('crisis_mode', False)
            
            performance_monitor.record_request(processing_time, blocked, crisis_mode)
            return result
        except Exception as e:
            performance_monitor.record_error()
            system_logger.log_error(e, {'function': func.__name__})
            raise
    return wrapper

def get_system_status() -> Dict[str, Any]:
    """Get current system status"""
    metrics = performance_monitor.get_metrics()
    percentiles = performance_monitor.get_percentiles()
    
    return {
        'status': 'operational',
        'metrics': metrics,
        'percentiles': percentiles,
        'timestamp': datetime.now().isoformat()
    }

# Initialize metrics collector
metrics_collector.load()

