#!/usr/bin/env python3
"""Validate project taxonomy structure.

This script ensures the project follows proper directory structure conventions
and prevents invalid directory naming patterns. It is used as a pre-commit hook
to maintain project organization standards.

What it validates:
1. Required directories: Checks for standard project directories (config, docs, etc.)
2. Invalid patterns: Prevents directories with problematic names (-copy, -backup, etc.)
3. Root-level file placement: Ensures documentation and report files are in appropriate directories

Exit codes:
    - 0: All checks passed
    - 1: Invalid directory name or file placement detected (fails pre-commit)

Usage:
    python3 scripts/validate_taxonomy.py

Related documentation:
    - scripts/README.md - Script documentation
    - .pre-commit-config.yaml - Pre-commit hook configuration
    - README.md#project-structure-validation - Project structure overview
"""
import fnmatch
import sys
from pathlib import Path


# Required directories (some may be optional depending on project)
# These are standard directories expected in most DDF projects
# Note: Currently set to warn only, not fail (uncomment sys.exit(1) to make strict)
REQUIRED_DIRS = [
    "config",  # Configuration files
    "docs",  # Documentation
    "scripts",  # Utility scripts
    "tests",  # Test files
    "workflows",  # Workflow scripts
]

# Check required directories
missing_dirs = [dir_name for dir_name in REQUIRED_DIRS if not Path(dir_name).is_dir()]

if missing_dirs:
    print(f"⚠️  Some expected directories not found: {', '.join(missing_dirs)}")
    # Don't fail for missing directories as project structure may vary
    # Uncomment the following line to make it strict:
    # sys.exit(1)

# Check for invalid directory names
# These patterns indicate problematic directory structures that should be avoided:
# - "-copy": Indicates duplicate/clone directories (violates DRY principle)
# - "-backup": Backup directories (should use version control instead)
# - "-partial": Incomplete/partial directories (indicates incomplete work)
invalid_patterns = ["-copy", "-backup", "-partial"]

# Recursively check all directories in the project
# Note: We use pathlib.Path().rglob() for cross-platform compatibility
for path in Path().rglob("*"):
    if not path.is_dir():
        continue
    # Skip hidden directories and common ignored paths
    if path.name.startswith(".") or path.name in [
        "node_modules",
        "venv",
        "__pycache__",
    ]:
        continue
    # Skip if any parent is in ignored paths
    if any(
        part in ["node_modules", "venv", "__pycache__", ".git"] for part in path.parts
    ):
        continue

    for pattern in invalid_patterns:
        if pattern in path.name:
            print(f"❌ Invalid directory name detected: {path}")
            sys.exit(1)

# Validate root-level file placement
# Files that should be in docs/ or appropriate subdirectories
ROOT_LEVEL_ALLOWED_FILES = {
    # Essential project files
    "README.md",
    "pyproject.toml",
    "package.json",
    "package-lock.json",
    "requirements-minimal.txt",
    "alembic.ini",
    "Makefile",
    ".gitignore",
    ".gitattributes",
    ".editorconfig",
    ".pre-commit-config.yaml",
    ".shellcheckrc",
    ".commitlintrc.json",
    ".env.example",
    # Configuration files
    "config.py",
    "main.py",
    # Directories (handled separately)
}

# Documentation files that should be in docs/ or subdirectories
# Patterns that indicate documentation/report files that belong in docs/
DOCUMENTATION_PATTERNS = [
    "*_REPORT.md",
    "*_PLAN.md",
    "*_SUMMARY.md",
    "*_DIRECTORY.md",
    "*_UPDATE.md",
    "*_GUIDE.md",
    "*_impact.md",
    "*_report.md",
    "*_demo.md",
    "*_results.md",
    "agents.md",
    "QUICK_START*.txt",
    "QUICK_REFERENCE.md",
    "*_RESOLVED.md",
    "*_IMPLEMENTATION.md",
]

# Files that are allowed at root level even if they match documentation patterns
# These are project-level documentation that should remain at root
ROOT_LEVEL_DOCUMENTATION_EXCEPTIONS = {
    "README.md",  # Always at root
    "CHANGELOG.md",  # Standard location
    "CONTRIBUTING.md",  # Standard location
    "LICENSE",  # Standard location
    "LICENSE.md",  # Standard location
}

# Check root-level files
root_path = Path()
violations = []

for file_path in root_path.iterdir():
    if not file_path.is_file():
        continue

    # Skip hidden files and allowed files
    if file_path.name.startswith("."):
        continue

    if file_path.name in ROOT_LEVEL_ALLOWED_FILES:
        continue

    # Skip documentation exceptions
    if file_path.name in ROOT_LEVEL_DOCUMENTATION_EXCEPTIONS:
        continue

    # Check if it's a documentation file that should be moved
    file_name = file_path.name
    is_documentation = False

    # Check against documentation patterns
    for pattern in DOCUMENTATION_PATTERNS:
        if fnmatch.fnmatch(file_name, pattern):
            is_documentation = True
            break

    # Also check if it's a markdown file (likely documentation)
    # Exclude essential project files already in ROOT_LEVEL_ALLOWED_FILES
    if file_path.suffix == ".md" and file_name not in ROOT_LEVEL_ALLOWED_FILES:
        is_documentation = True

    if is_documentation:
        violations.append(file_path.name)

if violations:
    print(
        "❌ Root-level documentation files detected that should be in docs/ or appropriate subdirectories:"
    )
    for violation in sorted(violations):
        print(f"   - {violation}")
    print("\n💡 Suggested locations:")
    print("   - Reports and summaries: docs/reports/ or docs/summaries/")
    print("   - Plans and guides: docs/plans/ or docs/guides/")
    print("   - Status updates: docs/status/ or docs/updates/")
    print("   - Quick references: docs/guides/")
    sys.exit(1)

sys.exit(0)
