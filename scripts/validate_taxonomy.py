#!/usr/bin/env python3
"""Validate project taxonomy structure.

This script ensures the project follows proper directory structure conventions
and prevents invalid directory naming patterns. It is used as a pre-commit hook
to maintain project organization standards.

What it validates:
1. Required directories: Checks for standard project directories (config, docs, etc.)
2. Invalid patterns: Prevents directories with problematic names (-copy, -backup, etc.)

Exit codes:
    - 0: All checks passed
    - 1: Invalid directory name detected (fails pre-commit)

Usage:
    python3 scripts/validate_taxonomy.py

Related documentation:
    - scripts/README.md - Script documentation
    - .pre-commit-config.yaml - Pre-commit hook configuration
    - README.md#project-structure-validation - Project structure overview
"""
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

sys.exit(0)
