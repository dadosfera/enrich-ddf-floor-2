#!/usr/bin/env python3
"""Validate project taxonomy structure."""
import sys
from pathlib import Path

# Required directories (some may be optional depending on project)
REQUIRED_DIRS = [
    "config",
    "docs",
    "scripts",
    "tests",
    "workflows",
]

# Check required directories
missing_dirs = [dir_name for dir_name in REQUIRED_DIRS if not Path(dir_name).is_dir()]

if missing_dirs:
    print(f"⚠️  Some expected directories not found: {', '.join(missing_dirs)}")
    # Don't fail for missing directories as project structure may vary
    # Uncomment the following line to make it strict:
    # sys.exit(1)

# Check for invalid directory names
invalid_patterns = ["-copy", "-backup", "-partial"]
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
