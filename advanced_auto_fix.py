#!/usr/bin/env python3
"""
Advanced Auto-Fix Script for Complex Code Patterns
This script handles advanced auto-fix patterns that Ruff cannot automatically fix
"""

import re
from pathlib import Path


def fix_logging_exception_patterns(content: str) -> str:
    """Fix TRY400: Replace logging.error with logging.exception in exception handlers"""
    # Pattern: except ...: ... logging.exception(...)
    pattern = r"(except[^:]*:\s*)([^:]*?)logging\.error\((.*?)\)"

    def replace_func(match):
        indent = match.group(1)
        before_code = match.group(2)
        args = match.group(3)
        return f"{indent}{before_code}logging.exception({args})"

    return re.sub(pattern, replace_func, content, flags=re.DOTALL)


def fix_elif_patterns(content: str) -> str:
    """Fix PLR5501: Convert 'else: if' to 'elif' patterns"""
    # Simple pattern: } else:\n    if
    pattern = r"}\s*else:\s*\n\s*if\s+([^:]+):"

    def replace_func(match):
        condition = match.group(1)
        return f" elif {condition}:"

    return re.sub(pattern, replace_func, content)


def fix_variable_overwrite(content: str) -> str:
    """Fix PLW2901: Variable overwritten in loop"""
    # Pattern: for line_item in lines: ... line_item = ...
    lines = content.split("\n")
    fixed_lines = []

    for i, line in enumerate(lines):
        if "for " in line and " in " in line and "=" in line:
            # Check if this line overwrites the loop variable
            loop_var = line.split("for ")[1].split(" in ")[0].strip()
            if f"{loop_var} =" in line:
                # Rename the loop variable to avoid conflict
                line = line.replace(f"for {loop_var} in", f"for {loop_var}_item in")
                # Replace all occurrences of the original variable with the new one
                line = line.replace(f"{loop_var} =", f"{loop_var}_item =")
        fixed_lines.append(line)

    return "\n".join(fixed_lines)


def fix_fstring_syntax(content: str) -> str:
    """Fix f-string syntax errors by adding missing braces"""
    # Pattern: f"..." with unclosed braces
    lines = content.split("\n")
    fixed_lines = []

    for line in lines:
        if 'f"' in line or "f'" in line:
            # Count braces
            open_count = line.count("{") - line.count("{{")
            close_count = line.count("}") - line.count("}}")

            if open_count > close_count:
                # Add missing closing braces
                line += "}" * (open_count - close_count)
        fixed_lines.append(line)

    return "\n".join(fixed_lines)


def apply_advanced_fixes(file_path: Path) -> bool:
    """Apply advanced auto-fixes to a single file"""
    try:
        content = file_path.read_text(encoding="utf-8")
        original_content = content

        # Apply fixes
        content = fix_logging_exception_patterns(content)
        content = fix_elif_patterns(content)
        content = fix_variable_overwrite(content)
        content = fix_fstring_syntax(content)

        if content != original_content:
            file_path.write_text(content, encoding="utf-8")
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
        Path("advanced_auto_fix.py"),  # Fix itself too
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
