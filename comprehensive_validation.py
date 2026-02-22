#!/usr/bin/env python3
"""
Comprehensive Codebase Validation and Optimization Script
Validates all Python files, checks structure, and identifies optimization opportunities
"""
import os
import sys
import ast
import importlib.util
from pathlib import Path
from typing import List, Dict, Tuple

class CodebaseValidator:
    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir)
        self.errors = []
        self.warnings = []
        self.optimizations = []
        self.stats = {
            'total_files': 0,
            'valid_files': 0,
            'invalid_files': 0,
            'total_classes': 0,
            'total_functions': 0,
            'import_issues': 0
        }
    
    def validate_python_file(self, filepath: Path) -> Tuple[bool, List[str]]:
        """Validate a single Python file"""
        errors = []
        warnings = []
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check syntax
            try:
                ast.parse(content)
            except SyntaxError as e:
                errors.append(f"Syntax error: {e.msg} at line {e.lineno}")
                return False, errors
            
            # Parse AST for analysis
            tree = ast.parse(content)
            
            # Check for common issues
            for node in ast.walk(tree):
                # Check for bare except clauses
                if isinstance(node, ast.ExceptHandler) and node.type is None:
                    warnings.append("Bare except clause found - should specify exception type")
                
                # Check for unused imports (basic check)
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        if alias.asname:
                            # Check if imported name is used
                            pass
            
            # Count classes and functions
            classes = [n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
            functions = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
            
            self.stats['total_classes'] += len(classes)
            self.stats['total_functions'] += len(functions)
            
            return True, warnings
            
        except Exception as e:
            errors.append(f"Error reading/parsing file: {str(e)}")
            return False, errors
    
    def check_imports(self, filepath: Path) -> List[str]:
        """Check if file can be imported"""
        issues = []
        try:
            spec = importlib.util.spec_from_file_location(
                filepath.stem, filepath
            )
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
        except Exception as e:
            issues.append(f"Import error: {str(e)}")
            self.stats['import_issues'] += 1
        return issues
    
    def analyze_structure(self) -> Dict:
        """Analyze codebase structure"""
        structure = {
            'core_files': [],
            'system_files': [],
            'integration_files': [],
            'utility_files': [],
            'duplicate_files': []
        }
        
        # Categorize files
        for filepath in self.root_dir.glob('*.py'):
            filename = filepath.name
            
            if filename == 'app.py':
                structure['core_files'].append(filename)
            elif filename == 'EthicalSystemIntegration.py' or 'Integration' in filename:
                structure['integration_files'].append(filename)
            elif 'System' in filename or 'Processor' in filename:
                structure['system_files'].append(filename)
            else:
                structure['utility_files'].append(filename)
        
        # Check for duplicate class names (files with similar names)
        filenames = [f.stem for f in self.root_dir.glob('*.py')]
        seen = set()
        for name in filenames:
            if name in seen:
                structure['duplicate_files'].append(name)
            seen.add(name)
        
        return structure
    
    def find_optimizations(self) -> List[str]:
        """Find optimization opportunities"""
        optimizations = []
        
        # Check for large files
        for filepath in self.root_dir.glob('*.py'):
            size = filepath.stat().st_size
            if size > 50000:  # 50KB
                optimizations.append(f"Large file: {filepath.name} ({size/1024:.1f}KB) - consider splitting")
        
        # Check for files with many classes
        for filepath in self.root_dir.glob('*.py'):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    tree = ast.parse(f.read())
                    classes = [n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
                    if len(classes) > 10:
                        optimizations.append(f"{filepath.name}: {len(classes)} classes - consider modularizing")
            except:
                pass
        
        return optimizations
    
    def validate_all(self) -> Dict:
        """Run comprehensive validation"""
        print("=" * 70)
        print("COMPREHENSIVE CODEBASE VALIDATION")
        print("=" * 70)
        print()
        
        # Get all Python files
        python_files = list(self.root_dir.glob('*.py'))
        self.stats['total_files'] = len(python_files)
        
        print(f"📁 Found {len(python_files)} Python files")
        print()
        
        # Validate each file
        print("🔍 Validating Python files...")
        print()
        
        for filepath in sorted(python_files):
            self.stats['total_files'] += 1
            is_valid, issues = self.validate_python_file(filepath)
            
            if is_valid:
                self.stats['valid_files'] += 1
                status = "✓"
            else:
                self.stats['invalid_files'] += 1
                status = "✗"
                self.errors.extend([f"{filepath.name}: {e}" for e in issues])
            
            if issues:
                self.warnings.extend([f"{filepath.name}: {w}" for w in issues])
            
            # Show status
            if not is_valid or issues:
                print(f"{status} {filepath.name}")
                for issue in issues:
                    print(f"   ⚠ {issue}")
        
        print()
        print("📊 Analyzing codebase structure...")
        structure = self.analyze_structure()
        
        print()
        print("⚡ Finding optimization opportunities...")
        optimizations = self.find_optimizations()
        
        return {
            'stats': self.stats,
            'errors': self.errors,
            'warnings': self.warnings,
            'optimizations': optimizations,
            'structure': structure
        }
    
    def print_report(self, results: Dict):
        """Print comprehensive report"""
        print()
        print("=" * 70)
        print("VALIDATION REPORT")
        print("=" * 70)
        print()
        
        # Statistics
        stats = results['stats']
        print("📈 STATISTICS")
        print(f"   Total Python files: {stats['total_files']}")
        print(f"   Valid files: {stats['valid_files']}")
        print(f"   Invalid files: {stats['invalid_files']}")
        print(f"   Total classes: {stats['total_classes']}")
        print(f"   Total functions: {stats['total_functions']}")
        print(f"   Import issues: {stats['import_issues']}")
        print()
        
        # Structure
        print("🏗️  CODEBASE STRUCTURE")
        structure = results['structure']
        print(f"   Core files: {len(structure['core_files'])}")
        print(f"   System files: {len(structure['system_files'])}")
        print(f"   Integration files: {len(structure['integration_files'])}")
        print(f"   Utility files: {len(structure['utility_files'])}")
        if structure['duplicate_files']:
            print(f"   ⚠ Duplicate file names: {structure['duplicate_files']}")
        print()
        
        # Errors
        if results['errors']:
            print("❌ ERRORS")
            for error in results['errors'][:10]:  # Show first 10
                print(f"   • {error}")
            if len(results['errors']) > 10:
                print(f"   ... and {len(results['errors']) - 10} more errors")
            print()
        
        # Warnings
        if results['warnings']:
            print("⚠️  WARNINGS")
            for warning in results['warnings'][:10]:  # Show first 10
                print(f"   • {warning}")
            if len(results['warnings']) > 10:
                print(f"   ... and {len(results['warnings']) - 10} more warnings")
            print()
        
        # Optimizations
        if results['optimizations']:
            print("⚡ OPTIMIZATION OPPORTUNITIES")
            for opt in results['optimizations']:
                print(f"   • {opt}")
            print()
        
        # Summary
        print("=" * 70)
        if not results['errors']:
            print("✅ VALIDATION PASSED - All files are syntactically valid")
        else:
            print("❌ VALIDATION FAILED - Some files have errors")
        print("=" * 70)

def main():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    validator = CodebaseValidator(root_dir)
    results = validator.validate_all()
    validator.print_report(results)
    
    return 0 if not results['errors'] else 1

if __name__ == '__main__':
    sys.exit(main())

