# Testing and Monitoring Guide

**Date:** February 2026  
**Status:** ✅ FULLY IMPLEMENTED (pipeline includes optional systems + output safety filter)

---

## Overview

Complete testing and monitoring framework has been implemented for the Kyosan Ethical AI System, including unit tests, integration tests, performance benchmarks, and a comprehensive monitoring/logging system. The ethical pipeline now invokes all optional systems (EthicalContext, CoreEthicalProcessor, BiasDetectionSystem, etc.) after Layer 4; outcomes are in `metadata.optional_systems`. API responses are filtered through OutputSafetyLayer in `app.py`. See `docs/INTEGRATION_STATUS_VERIFICATION.md` for integration details.

---

## 1. Unit Tests ✅

### Location: `tests/test_harm_detection.py`

Tests for `HarmDetectionLayer`:
- ✅ Normal input handling
- ✅ Crisis mode bypass functionality
- ✅ Sensitivity parameter adjustment
- ✅ Context awareness parameter

### Location: `tests/test_integrated_processor.py`

Tests for `IntegratedEthicalProcessor`:
- ✅ System initialization
- ✅ Always active systems initialization
- ✅ Process input structure validation
- ✅ Crisis mode processing

**Test Results:** All unit tests passing ✅

---

## 2. Integration Tests ✅

### Location: `tests/test_integration.py`

Full pipeline integration tests:
- ✅ Complete pipeline with normal input
- ✅ Complete pipeline with crisis mode
- ✅ Multi-turn conversation handling
- ✅ Error handling and graceful degradation

**Test Results:** All integration tests passing ✅

---

## 3. Performance Benchmarks ✅

### Location: `tests/test_performance.py`

Performance metrics:
- ✅ **Initialization Time:** System startup benchmark
- ✅ **Single Request Latency:** Average processing time per request
- ✅ **Throughput:** Requests per second capacity
- ✅ **Memory Usage:** Memory efficiency tracking

**Benchmark Results:**
- Initialization: < 5 seconds ✅
- Average latency: < 2 seconds ✅
- Throughput: > 1 request/second ✅
- Memory usage: < 500 MB ✅

---

## 4. Monitoring and Logging Framework ✅

### Location: `monitoring.py`

#### Components:

1. **PerformanceMonitor**
   - Tracks total requests
   - Monitors blocked vs allowed requests
   - Calculates average processing time
   - Records errors
   - Tracks crisis mode activations
   - Provides percentile metrics (p50, p75, p90, p95, p99)

2. **SystemLogger**
   - Enhanced logging with context
   - Request logging with parameters
   - Error logging with tracebacks
   - System event logging

3. **MetricsCollector**
   - Collects metrics snapshots
   - Stores metrics history (last 1000)
   - Saves/loads metrics to/from JSON

4. **Performance Decorator**
   - `@monitor_performance` decorator
   - Automatic performance tracking
   - Error recording

#### Integration with app.py:

- ✅ Monitoring automatically enabled on startup
- ✅ All `/api/chat` requests are monitored
- ✅ Errors are logged with context
- ✅ Performance metrics collected automatically

#### New API Endpoints:

**GET `/api/status`**
- Returns system status and current metrics
- Example response:
```json
{
  "status": "operational",
  "metrics": {
    "requests_total": 100,
    "requests_blocked": 5,
    "requests_allowed": 95,
    "average_processing_time": 0.5,
    "errors": 0,
    "crisis_mode_activations": 10
  },
  "percentiles": {
    "p50": 0.4,
    "p75": 0.6,
    "p90": 0.8,
    "p95": 1.0,
    "p99": 1.5
  },
  "timestamp": "2025-12-25T16:50:00"
}
```

**GET `/api/metrics`**
- Returns detailed performance metrics
- Includes percentiles for processing times

---

## Running Tests

### Run All Tests

```bash
python3 run_tests.py
```

### Run Specific Test Suite

```bash
# Unit tests
python3 -m unittest tests.test_harm_detection
python3 -m unittest tests.test_integrated_processor

# Integration tests
python3 -m unittest tests.test_integration

# Performance benchmarks
python3 -m unittest tests.test_performance
```

### Test Output

```
================================================================================
TEST SUMMARY
================================================================================
Tests run: 16
Successes: 16
Failures: 0
Errors: 0
================================================================================
```

---

## Monitoring Usage

### Check System Status

```bash
curl http://localhost:5000/api/status
```

### Get Performance Metrics

```bash
curl http://localhost:5000/api/metrics
```

### View Logs

Logs are automatically written to:
- **File:** `logs/ethical_ai.log`
- **Console:** Standard output

### Log Format

```
2025-12-25 16:50:00 - EthicalAI - INFO - Processing request
2025-12-25 16:50:01 - EthicalAI - ERROR - Error occurred: ...
```

---

## Metrics Available

### Performance Metrics

- `requests_total`: Total number of requests processed
- `requests_blocked`: Number of requests blocked by ethical system
- `requests_allowed`: Number of requests allowed through
- `average_processing_time`: Average time to process a request (seconds)
- `total_processing_time`: Cumulative processing time
- `errors`: Number of errors encountered
- `crisis_mode_activations`: Number of times crisis mode was activated

### Percentiles

- `p50`: Median processing time
- `p75`: 75th percentile processing time
- `p90`: 90th percentile processing time
- `p95`: 95th percentile processing time
- `p99`: 99th percentile processing time

---

## Test Coverage

### Components Tested

✅ HarmDetectionLayer  
✅ IntegratedEthicalProcessor  
✅ System initialization  
✅ Always active systems  
✅ Processing pipeline  
✅ Crisis mode functionality  
✅ Error handling  
✅ Performance metrics  

### Test Statistics

- **Total Tests:** 16
- **Passing:** 16 (100%)
- **Failures:** 0
- **Errors:** 0

---

## Best Practices

### For Development

1. Run tests before committing changes
2. Check metrics after significant changes
3. Monitor logs for errors
4. Review performance benchmarks regularly

### For Production

1. Enable monitoring (default: enabled)
2. Set up log rotation for `logs/ethical_ai.log`
3. Monitor `/api/status` endpoint
4. Track metrics over time
5. Set up alerts for high error rates

---

## Files Created

1. ✅ `tests/__init__.py` - Test package
2. ✅ `tests/test_harm_detection.py` - Unit tests for harm detection
3. ✅ `tests/test_integrated_processor.py` - Unit tests for processor
4. ✅ `tests/test_integration.py` - Integration tests
5. ✅ `tests/test_performance.py` - Performance benchmarks
6. ✅ `monitoring.py` - Monitoring and logging framework
7. ✅ `run_tests.py` - Test runner script
8. ✅ `TESTING_AND_MONITORING_GUIDE.md` - This guide

---

## Integration Status

✅ **Monitoring integrated into app.py**  
✅ **All endpoints monitored**  
✅ **Error logging active**  
✅ **Performance tracking enabled**  
✅ **Status endpoint available**  
✅ **Metrics endpoint available**  

---

## Conclusion

All testing and monitoring enhancements have been successfully implemented:

- ✅ 16 unit and integration tests (all passing)
- ✅ Performance benchmarks (all passing)
- ✅ Comprehensive monitoring framework (operational)
- ✅ Logging system (active)
- ✅ Metrics collection (active)
- ✅ API endpoints for status/metrics (available)

**Status:** PRODUCTION READY 🚀

---

*Last Updated: December 25, 2025*

