#!/usr/bin/env python3
"""Validate project taxonomy structure.

This script ensures the project follows proper directory structure conventions
and prevents invalid directory naming patterns. It is used as a pre-commit hook
to maintain project organization standards.

What it validates:
1. Required directories: Checks for standard project directories (config, docs, etc.)
2. Invalid patterns: Prevents directories with problematic names (-copy, -backup, etc.)
3. Root-level directory violations: Prevents /active and /scripts directories at root level
4. Root-level file placement: Ensures backup files, log files, and documentation files are in appropriate directories

Exit codes:
    - 0: All checks passed
    - 1: Invalid directory name or file placement detected (fails pre-commit)

Usage:
    python3 workflows/scripts/validate_taxonomy.py

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
# Note: scripts/ is NOT in REQUIRED_DIRS because it violates "Nothing new goes in root" rule
REQUIRED_DIRS = [
    "config",  # Configuration files
    "docs",  # Documentation
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

# Check for root-level /active directory violation
# Active plans should be in docs/plans/active/, not at root level
active_dir = Path("active")
if active_dir.is_dir():
    print("❌ Root-level 'active/' directory detected.")
    print("   Active plans should be in docs/plans/active/, not at root level.")
    print("   Please move files from active/ to docs/plans/active/")
    sys.exit(1)

# Check for root-level /scripts directory violation
# Scripts should live under workflows/ (e.g., workflows/scripts/, workflows/cost/, workflows/quality/) or docs/scripts/, not at root level
# Per folder structure discipline: "Nothing new goes in the project root"
scripts_dir = Path("scripts")
if scripts_dir.is_dir():
    print("❌ Root-level 'scripts/' directory detected.")
    print(
        "   Scripts should live under workflows/ (e.g., workflows/scripts/, workflows/cost/, workflows/quality/) or docs/scripts/, not at root level."
    )
    print("   Per folder structure discipline: 'Nothing new goes in the project root'")
    print(
        "   Please move files from scripts/ to workflows/ (for example, workflows/scripts/, workflows/cost/, workflows/quality/) or docs/scripts/."
    )
    sys.exit(1)

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
backup_files = []
log_files = []

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

    file_name = file_path.name
    file_suffix = file_path.suffix.lower()

    # Check for backup files (.bak, .backup, etc.)
    if (
        file_suffix in [".bak", ".backup"]
        or file_name.endswith(".bak")
        or file_name.endswith(".backup")
    ):
        backup_files.append(file_path.name)
        continue

    # Check for log files (.log, .txt log files)
    if file_suffix == ".log" or (file_suffix == ".txt" and "log" in file_name.lower()):
        log_files.append(file_path.name)
        continue

    # Check if it's a documentation file that should be moved
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

# Check for backup files at root level
if backup_files:
    print("❌ Root-level backup files detected that should be cleaned up or moved:")
    for backup_file in sorted(backup_files):
        print(f"   - {backup_file}")
    print("\n💡 Suggested actions:")
    print("   - Temporary backups: Move to .tmp/ or delete if no longer needed")
    print("   - Long-term backups: Move to backup/ directory")
    print("   - Best practice: Clean up .bak files after verifying changes")
    sys.exit(1)

# Check for log files at root level
if log_files:
    print("❌ Root-level log files detected that should be in logs/ directory:")
    for log_file in sorted(log_files):
        print(f"   - {log_file}")
    print("\n💡 Suggested locations:")
    print("   - Application logs: logs/ directory")
    print("   - Temporary logs: .tmp/ directory")
    print("   - Build/test logs: logs/build/ or logs/test/")
    sys.exit(1)

# Check for documentation files at root level
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
