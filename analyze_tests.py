#!/usr/bin/env python3
import re

def analyze_test_file(filename):
    """Analyze test file to understand its structure."""
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all test classes and functions
    test_classes = []
    test_functions = []
    imports = []
    fixtures = []
    
    lines = content.split('\n')
    current_decorator = None
    
    for i, line in enumerate(lines, 1):
        line = line.strip()
        
        # Track imports
        if line.startswith('import ') or line.startswith('from '):
            imports.append((i, line))
            continue
            
        # Track decorators
        if line.startswith('@'):
            current_decorator = line
            continue
            
        # Find test class definitions
        if line.startswith('class ') and 'Test' in line:
            class_name = line.split('(')[0].replace('class ', '').replace(':', '')
            test_classes.append((i, class_name, current_decorator))
            current_decorator = None
            
        # Find test function definitions  
        elif line.startswith('def test_'):
            func_name = line.split('(')[0].replace('def ', '')
            test_functions.append((i, func_name, current_decorator))
            current_decorator = None
            
        # Find pytest fixtures
        elif line.startswith('def ') and current_decorator and 'fixture' in current_decorator:
            func_name = line.split('(')[0].replace('def ', '')
            fixtures.append((i, func_name, current_decorator))
            current_decorator = None
        
        # Reset decorator if we hit a non-decorator, non-def line
        elif line and not line.startswith(' ') and not line.startswith('#'):
            current_decorator = None
    
    return {
        'imports': imports[:10],  # First 10 imports
        'test_classes': test_classes,
        'test_functions': test_functions,
        'fixtures': fixtures,
        'total_lines': len(lines)
    }

if __name__ == '__main__':
    result = analyze_test_file('backend/sentiment_analysis/test_sentiment_analysis.py')
    
    print(f"Test File Analysis: backend/sentiment_analysis/test_sentiment_analysis.py")
    print(f"Total Lines: {result['total_lines']}")
    print()
    
    print("Key Imports (first 10):")
    for line_num, import_line in result['imports']:
        print(f"  Line {line_num}: {import_line}")
    print()
    
    print(f"Test Classes ({len(result['test_classes'])}):")
    for line_num, name, decorator in result['test_classes']:
        decorator_str = f" ({decorator})" if decorator else ""
        print(f"  Line {line_num}: {name}{decorator_str}")
    print()
    
    print(f"Test Functions ({len(result['test_functions'])}):")
    for line_num, name, decorator in result['test_functions'][:20]:  # Show first 20
        decorator_str = f" ({decorator})" if decorator else ""
        print(f"  Line {line_num}: {name}{decorator_str}")
    
    if len(result['test_functions']) > 20:
        print(f"  ... and {len(result['test_functions']) - 20} more test functions")
    print()
    
    print(f"Fixtures ({len(result['fixtures'])}):")
    for line_num, name, decorator in result['fixtures']:
        print(f"  Line {line_num}: {name} ({decorator})")