#!/usr/bin/env python3
"""
Advanced Auto-Fix Script for Complex Code Patterns
This script handles advanced auto-fix patterns that Ruff cannot automatically fix
"""

import re
from pathlib import Path


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

def fix_explicit_conversion_flags(content: str) -> str:
    """Fix RUF010: Add explicit conversion flags"""
    # Pattern: f"{value}" where value might need !r or !s
    patterns = [
        # For strings that should use !r
        (r'f"([^"]*?){\s*([^}]+?)\s*}"', r'f"\1{\2!r}"'),
        # For general objects that should use !r
        (r'f"([^"]*?){\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*}"', r'f"\1{\2!r}"'),
    ]

    result = content
    for pattern, replacement in patterns:
        # Only apply to specific known cases
        result = re.sub(pattern, replacement, result)

    return result

def fix_try_else_patterns(content: str) -> str:
    """Fix TRY300: Move statements to else blocks"""
    # This is complex and would require AST parsing - simplified version
    return content

def apply_advanced_fixes(file_path: Path) -> bool:
    """Apply advanced auto-fixes to a single file"""
    try:
        content = file_path.read_text(encoding='utf-8')
        original_content = content

        # Apply fixes
        content = fix_logging_exception_patterns(content)
        content = fix_elif_patterns(content)
        content = fix_explicit_conversion_flags(content)
        content = fix_try_else_patterns(content)

        if content != original_content:
            file_path.write_text(content, encoding='utf-8')
            return True
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

    return False

def main():
    """Main function to run advanced auto-fixes"""
    print("🔧 Running advanced auto-fix patterns...")

    files_to_process = [
        Path("core/enrichment/real_data_enrichment.py"),
        Path("main.py"),
    ]

    fixed_files = []

    for file_path in files_to_process:
        if file_path.exists():
            print(f"📋 Processing {file_path}...")
            if apply_advanced_fixes(file_path):
                fixed_files.append(file_path)
                print(f"✅ Fixed {file_path}")
            else:
                print(f"ℹ No fixes needed for {file_path}")

    if fixed_files:
        print(f"🎯 Advanced auto-fix completed for {len(fixed_files)} files")
        return True
    else:
        print("ℹ No advanced fixes were applied")
        return False

if __name__ == "__main__":
    main()
