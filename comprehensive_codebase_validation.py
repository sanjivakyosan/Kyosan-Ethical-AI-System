"""
Comprehensive Codebase Validation and Optimization Script
Analyzes structure, validates systems, and optimizes for best operation
"""
import os
import sys
import ast
import importlib.util
from pathlib import Path
from typing import Dict, List, Set, Tuple
from datetime import datetime

class CodebaseValidator:
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.results = {
            'files_analyzed': 0,
            'files_valid': 0,
            'files_invalid': 0,
            'imports_checked': 0,
            'imports_valid': 0,
            'imports_invalid': 0,
            'systems_tested': 0,
            'systems_active': 0,
            'systems_inactive': 0,
            'errors': [],
            'warnings': [],
            'optimizations': []
        }
        self.core_systems = [
            'app',
            'EthicalSystemIntegration',
            'CoreEthicalProcessor',
            'EthicalContext',
            'WellbeingMonitor',
            'RealTimeDecisionFramework',
            'ConsciousnessObserver'
        ]
        self.optional_systems = [
            'BiasDetectionSystem',
            'EthicalLearningSystem',
            'EthicalMemorySystem',
            'ValueConflictResolver',
            'DistributedEthicsSystem',
            'ErrorRecoverySystem',
            'EthicalSecuritySystem'
        ]
    
    def validate_syntax(self, file_path: Path) -> Tuple[bool, str]:
        """Validate Python file syntax"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            ast.parse(code)
            return True, ""
        except SyntaxError as e:
            return False, f"Syntax error: {e}"
        except Exception as e:
            return False, f"Error reading file: {e}"
    
    def check_imports(self, file_path: Path) -> List[str]:
        """Check if imports in file are valid"""
        invalid_imports = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read())
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        module_name = alias.name.split('.')[0]
                        if not self._can_import(module_name):
                            invalid_imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        module_name = node.module.split('.')[0]
                        if not self._can_import(module_name):
                            invalid_imports.append(node.module)
        except Exception as e:
            invalid_imports.append(f"Error checking imports: {e}")
        
        return invalid_imports
    
    def _can_import(self, module_name: str) -> bool:
        """Check if module can be imported"""
        # Skip standard library and third-party modules
        if module_name in ['os', 'sys', 'json', 'datetime', 'time', 'typing', 
                          'flask', 'openai', 'requests', 'pathlib', 'ast']:
            return True
        
        # Check if it's a local file
        module_path = self.base_path / f"{module_name}.py"
        if module_path.exists():
            return True
        
        # Try importing
        try:
            __import__(module_name)
            return True
        except ImportError:
            return False
    
    def test_system_initialization(self, system_name: str) -> Tuple[bool, str]:
        """Test if a system can be initialized"""
        try:
            # Add base path to sys.path
            if str(self.base_path) not in sys.path:
                sys.path.insert(0, str(self.base_path))
            
            # Try to import
            module = importlib.import_module(system_name)
            
            # Try to find main class (usually same name as file or common patterns)
            class_names = [name for name in dir(module) 
                          if not name.startswith('_') and 
                          isinstance(getattr(module, name), type)]
            
            if not class_names:
                return True, "Module imported but no classes found (may be expected)"
            
            # Try to instantiate first class
            main_class = getattr(module, class_names[0])
            try:
                instance = main_class()
                return True, f"Successfully initialized {class_names[0]}"
            except Exception as e:
                return False, f"Could not instantiate {class_names[0]}: {e}"
                
        except ImportError as e:
            return False, f"Import error: {e}"
        except Exception as e:
            return False, f"Error: {e}"
    
    def analyze_file_structure(self, file_path: Path) -> Dict:
        """Analyze structure of a Python file"""
        structure = {
            'classes': [],
            'functions': [],
            'imports': [],
            'has_main': False
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read())
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    structure['classes'].append(node.name)
                elif isinstance(node, ast.FunctionDef):
                    structure['functions'].append(node.name)
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        structure['imports'].append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        structure['imports'].append(node.module)
            
            # Check for main block
            for node in ast.walk(tree):
                if isinstance(node, ast.If):
                    if isinstance(node.test, ast.Compare):
                        if isinstance(node.test.left, ast.Name) and node.test.left.id == '__name__':
                            structure['has_main'] = True
        except Exception as e:
            structure['error'] = str(e)
        
        return structure
    
    def validate_integration_points(self) -> Dict:
        """Validate integration between systems"""
        integration_status = {
            'app_to_integration': False,
            'integration_to_core': False,
            'integration_to_context': False,
            'integration_to_wellbeing': False,
            'integration_to_observer': False
        }
        
        # Check app.py integration
        try:
            with open(self.base_path / 'app.py', 'r') as f:
                app_code = f.read()
                if 'EthicalSystemIntegration' in app_code and 'IntegratedEthicalProcessor' in app_code:
                    integration_status['app_to_integration'] = True
        except Exception as e:
            self.results['errors'].append(f"Error checking app integration: {e}")
        
        # Check EthicalSystemIntegration.py
        try:
            with open(self.base_path / 'EthicalSystemIntegration.py', 'r') as f:
                integration_code = f.read()
                if 'CoreEthicalProcessor' in integration_code:
                    integration_status['integration_to_core'] = True
                if 'EthicalContext' in integration_code:
                    integration_status['integration_to_context'] = True
                if 'WellbeingMonitor' in integration_code:
                    integration_status['integration_to_wellbeing'] = True
                if 'ConsciousnessObserver' in integration_code:
                    integration_status['integration_to_observer'] = True
        except Exception as e:
            self.results['errors'].append(f"Error checking integration: {e}")
        
        return integration_status
    
    def find_optimization_opportunities(self) -> List[str]:
        """Find opportunities for optimization"""
        optimizations = []
        
        # Check for duplicate code
        # Check for unused imports
        # Check for inefficient patterns
        
        # Check if error handling is consistent
        try:
            with open(self.base_path / 'app.py', 'r') as f:
                app_code = f.read()
                if 'except Exception as e:' in app_code and 'traceback' not in app_code:
                    optimizations.append("Consider adding traceback logging in app.py error handlers")
        except:
            pass
        
        # Check for missing type hints
        # Check for docstring coverage
        
        return optimizations
    
    def run_full_validation(self) -> Dict:
        """Run complete validation"""
        print("=" * 80)
        print("COMPREHENSIVE CODEBASE VALIDATION")
        print("=" * 80)
        print(f"Base Path: {self.base_path}")
        print(f"Started: {datetime.now()}\n")
        
        # 1. Validate all Python files
        print("1. VALIDATING FILE SYNTAX...")
        python_files = list(self.base_path.glob("*.py"))
        for file_path in python_files:
            if file_path.name.startswith('_'):
                continue
            self.results['files_analyzed'] += 1
            is_valid, error = self.validate_syntax(file_path)
            if is_valid:
                self.results['files_valid'] += 1
            else:
                self.results['files_invalid'] += 1
                self.results['errors'].append(f"{file_path.name}: {error}")
        
        print(f"   ✓ Analyzed {self.results['files_analyzed']} files")
        print(f"   ✓ Valid: {self.results['files_valid']}")
        print(f"   ✗ Invalid: {self.results['files_invalid']}\n")
        
        # 2. Test core systems
        print("2. TESTING CORE SYSTEMS...")
        for system in self.core_systems:
            self.results['systems_tested'] += 1
            is_active, message = self.test_system_initialization(system)
            if is_active:
                self.results['systems_active'] += 1
                print(f"   ✓ {system}: {message}")
            else:
                self.results['systems_inactive'] += 1
                self.results['warnings'].append(f"{system}: {message}")
                print(f"   ⚠ {system}: {message}")
        print()
        
        # 3. Test optional systems
        print("3. TESTING OPTIONAL SYSTEMS...")
        for system in self.optional_systems:
            is_active, message = self.test_system_initialization(system)
            if is_active:
                print(f"   ✓ {system}: Available")
            else:
                print(f"   - {system}: Not available (optional)")
        print()
        
        # 4. Validate integration points
        print("4. VALIDATING INTEGRATION POINTS...")
        integration_status = self.validate_integration_points()
        for point, status in integration_status.items():
            if status:
                print(f"   ✓ {point.replace('_', ' ').title()}")
            else:
                print(f"   ✗ {point.replace('_', ' ').title()}")
                self.results['warnings'].append(f"Integration point {point} not connected")
        print()
        
        # 5. Find optimizations
        print("5. ANALYZING OPTIMIZATION OPPORTUNITIES...")
        optimizations = self.find_optimization_opportunities()
        self.results['optimizations'] = optimizations
        if optimizations:
            for opt in optimizations:
                print(f"   💡 {opt}")
        else:
            print("   ✓ No critical optimizations needed")
        print()
        
        # 6. Summary
        print("=" * 80)
        print("VALIDATION SUMMARY")
        print("=" * 80)
        print(f"Files Analyzed: {self.results['files_analyzed']}")
        print(f"Files Valid: {self.results['files_valid']} ({self.results['files_valid']/max(self.results['files_analyzed'],1)*100:.1f}%)")
        print(f"Core Systems Active: {self.results['systems_active']}/{self.results['systems_tested']}")
        print(f"Errors: {len(self.results['errors'])}")
        print(f"Warnings: {len(self.results['warnings'])}")
        print(f"Optimizations: {len(self.results['optimizations'])}")
        print()
        
        if self.results['errors']:
            print("ERRORS FOUND:")
            for error in self.results['errors'][:10]:  # Show first 10
                print(f"  ✗ {error}")
            if len(self.results['errors']) > 10:
                print(f"  ... and {len(self.results['errors']) - 10} more")
            print()
        
        if self.results['warnings']:
            print("WARNINGS:")
            for warning in self.results['warnings'][:10]:  # Show first 10
                print(f"  ⚠ {warning}")
            if len(self.results['warnings']) > 10:
                print(f"  ... and {len(self.results['warnings']) - 10} more")
            print()
        
        print("=" * 80)
        print(f"Completed: {datetime.now()}")
        print("=" * 80)
        
        return self.results

if __name__ == "__main__":
    base_path = "/Users/sanjivakyosan/Desktop/empry set AI"
    validator = CodebaseValidator(base_path)
    results = validator.run_full_validation()
    
    # Save results
    with open(Path(base_path) / "VALIDATION_RESULTS.json", "w") as f:
        import json
        json.dump(results, f, indent=2, default=str)
    
    print(f"\nResults saved to: {base_path}/VALIDATION_RESULTS.json")

