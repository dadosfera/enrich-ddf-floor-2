#!/usr/bin/env python3
"""
Advanced Auto-Fix Script for Complex Code Patterns
This script handles advanced auto-fix patterns that Ruff cannot automatically fix
"""

import logging
import re
from pathlib import Path


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def fix_logging_exception_patterns(content: str) -> str:
    """Fix TRY400: Replace logging.error with logging.exception in exception handlers"""
    # Pattern: except ...: ... logging.error(...)
    pattern = r'(except[^:]*:\s*)([^:]*?)logging\.error\((.*?)\)'

    def replace_func(match):
        indent = match.group(1)
        before_code = match.group(2)
        args = match.group(3)
        return f"{indent}{before_code}logging.exception({args})"

    return re.sub(pattern, replace_func, content, flags=re.DOTALL)

def fix_elif_patterns(content: str) -> str:
    """Fix PLR5501: Convert 'else: if' to 'elif' patterns"""
    # Simple pattern: } else:\n    if
    pattern = r'}\s*else:\s*\n\s*if\s+([^:]+):'

    def replace_func(match):
        condition = match.group(1)
        return f" elif {condition}:"

    return re.sub(pattern, replace_func, content)

def fix_unused_variables(content: str) -> str:
    """Fix F841: Remove unused variable assignments"""
    lines = content.split('\n')
    fixed_lines = []

    for line in lines:
        # Simple pattern for unused timestamp variables in tests
        if 'timestamp = datetime.now()' in line and '# F841' not in line:
            # Comment out or remove the line
            continue
        fixed_lines.append(line)

    return '\n'.join(fixed_lines)

def fix_loop_variable_overwrite(content: str) -> str:
    """Fix PLW2901: Rename loop variables to avoid overwriting"""
    # This is a complex pattern that requires careful analysis
    # For now, we'll add a comment to indicate manual review needed
    lines = content.split('\n')
    fixed_lines = []

    for _i, line in enumerate(lines):
        if 'for' in line and 'in' in line:
            # Check if this might be a problematic loop variable
            if any(var in line for var in ['line', 'item', 'data', 'result']):
                # Add a comment for manual review
                fixed_lines.append(f"{line}  # TODO: Review loop variable naming (PLW2901)")
            else:
                fixed_lines.append(line)
        else:
            fixed_lines.append(line)

    return '\n'.join(fixed_lines)

def fix_fstring_syntax(content: str) -> str:
    """Fix f-string syntax errors by adding missing braces"""
    # This is a simplified approach and might not catch all cases
    # It specifically targets unclosed braces in f-strings
    lines = content.split('\n')
    fixed_lines = []

    for current_line in lines:
        # Fix f-strings with missing closing braces
        if 'f"' in current_line or "f'" in current_line:
            # Count braces
            open_count = current_line.count('{') - current_line.count('{{')
            close_count = current_line.count('}') - current_line.count('}}')
            
            if open_count > close_count:
                # Add missing closing braces
                current_line += '}' * (open_count - close_count)
        fixed_lines.append(current_line)

    return '\n'.join(fixed_lines)

def apply_advanced_fixes(file_path: Path) -> bool:
    """Apply advanced auto-fixes to a single file"""
    try:
        content = file_path.read_text(encoding='utf-8')
        original_content = content

        # Apply fixes
        content = fix_logging_exception_patterns(content)
        content = fix_elif_patterns(content)
        content = fix_unused_variables(content)
        content = fix_loop_variable_overwrite(content)
        content = fix_fstring_syntax(content)

        if content != original_content:
            file_path.write_text(content, encoding='utf-8')
            return True
    except Exception as e:
        logging.error(f"Error processing {file_path}: {e}")
    return False

def main():
    """Main function to run advanced auto-fixes"""
    logging.info("🔧 Running advanced auto-fix patterns...")

    # Find Python files with issues
    python_files = [
        Path("core/enrichment/real_data_enrichment.py"),
        Path("main.py"),
        Path("demo_enrichment.py"),
        Path("test_real_enrichment.py"),
    ]

    # Also process test files
    test_files = list(Path("tests").rglob("*.py"))
    python_files.extend(test_files)

    fixed_files = []

    for file_path in python_files:
        if file_path.exists():
            logging.info(f"📋 Processing {file_path}...")
            if apply_advanced_fixes(file_path):
                fixed_files.append(file_path)
                logging.info(f"✅ Fixed {file_path}")
            else:
                logging.info(f"ℹ No fixes needed for {file_path}")

    if fixed_files:
        logging.info(f"🎯 Advanced auto-fix completed for {len(fixed_files)} files")
        return True
    else:
        logging.info("ℹ No advanced fixes were applied")
        return False

if __name__ == "__main__":
    main()
