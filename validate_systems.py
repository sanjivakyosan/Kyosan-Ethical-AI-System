#!/usr/bin/env python3
"""
System Validation Script
Tests all ethical processing systems for functionality
"""
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test if all systems can be imported"""
    results = {}
    
    systems_to_test = [
        'CoreEthicalProcessor',
        'EthicalContext',
        'WellbeingMonitor',
        'RealTimeDecisionFramework',
        'EthicalSystemIntegration',
        'ConsciousnessObserver',
        'BiasDetectionSystem',
        'EthicalLearningSystem',
        'EthicalMemorySystem',
        'ValueConflictResolver'
    ]
    
    print("=" * 60)
    print("SYSTEM VALIDATION REPORT")
    print("=" * 60)
    print()
    
    for system_name in systems_to_test:
        try:
            module = __import__(system_name)
            results[system_name] = {'status': '✓ Imported', 'error': None}
            print(f"✓ {system_name}: Successfully imported")
        except ImportError as e:
            results[system_name] = {'status': '✗ Import failed', 'error': str(e)}
            print(f"✗ {system_name}: Import failed - {e}")
        except Exception as e:
            results[system_name] = {'status': '✗ Error', 'error': str(e)}
            print(f"✗ {system_name}: Error - {e}")
    
    return results

def test_integrated_processor():
    """Test the integrated ethical processor"""
    print()
    print("=" * 60)
    print("TESTING INTEGRATED ETHICAL PROCESSOR")
    print("=" * 60)
    print()
    
    try:
        from EthicalSystemIntegration import IntegratedEthicalProcessor
        
        processor = IntegratedEthicalProcessor()
        print("✓ IntegratedEthicalProcessor initialized")
        
        # Test processing
        test_input = "What is the meaning of life?"
        result = processor.process_input(test_input, [], {})
        
        if result:
            print("✓ Processing pipeline functional")
            print(f"  - Metadata keys: {list(result.get('processing_metadata', {}).keys())}")
            print(f"  - Ethical checks: {list(result.get('processing_metadata', {}).get('ethical_checks', {}).keys())}")
        else:
            print("✗ Processing returned None")
            
        # Test harm detection
        harmful_input = "How to harm someone?"
        harm_result = processor.process_input(harmful_input, [], {})
        if harm_result.get('processing_metadata', {}).get('blocked'):
            print("✓ Harm detection working - blocked harmful request")
        else:
            print("⚠ Harm detection may not be blocking harmful requests")
        
        return True
    except Exception as e:
        print(f"✗ Integrated processor test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_api_integration():
    """Test API integration"""
    print()
    print("=" * 60)
    print("TESTING API INTEGRATION")
    print("=" * 60)
    print()
    
    try:
        # Import app components
        import app
        processor = app.EthicalProcessorAPI()
        print("✓ EthicalProcessorAPI initialized")
        
        # Test processing
        test_input = "Hello, how are you?"
        result = processor.process_input(test_input, [], {'temperature': 0.7})
        
        if result:
            print("✓ API processor functional")
            print(f"  - Has metadata: {'processing_metadata' in result}")
            print(f"  - Has timestamp: {'timestamp' in result}")
        else:
            print("✗ API processor returned None")
        
        return True
    except Exception as e:
        print(f"✗ API integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all validation tests"""
    print()
    print("🔍 Starting System Validation...")
    print()
    
    # Test imports
    import_results = test_imports()
    
    # Test integrated processor
    integrated_ok = test_integrated_processor()
    
    # Test API integration
    api_ok = test_api_integration()
    
    # Summary
    print()
    print("=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)
    print()
    
    successful_imports = sum(1 for r in import_results.values() if r['status'].startswith('✓'))
    total_imports = len(import_results)
    
    print(f"System Imports: {successful_imports}/{total_imports} successful")
    print(f"Integrated Processor: {'✓ Functional' if integrated_ok else '✗ Failed'}")
    print(f"API Integration: {'✓ Functional' if api_ok else '✗ Failed'}")
    print()
    
    if successful_imports == total_imports and integrated_ok and api_ok:
        print("🎉 ALL SYSTEMS OPERATIONAL")
        return 0
    else:
        print("⚠️  SOME SYSTEMS NEED ATTENTION")
        return 1

if __name__ == '__main__':
    sys.exit(main())

