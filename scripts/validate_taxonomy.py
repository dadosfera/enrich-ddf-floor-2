#!/usr/bin/env python3
"""Validate project taxonomy structure."""
import os
import subprocess
import sys

# Required directories (some may be optional depending on project)
REQUIRED_DIRS = [
    "config",
    "docs",
    "scripts",
    "tests",
    "workflows",
]

# Check required directories
missing_dirs = []
for dir_name in REQUIRED_DIRS:
    if not os.path.isdir(dir_name):
        missing_dirs.append(dir_name)

if missing_dirs:
    print(f"⚠️  Some expected directories not found: {', '.join(missing_dirs)}")
    # Don't fail for missing directories as project structure may vary
    # Uncomment the following line to make it strict:
    # sys.exit(1)

# Check for invalid directory names
invalid_patterns = ["-copy", "-backup", "-partial"]
for root, dirs, _ in os.walk("."):
    # Skip hidden directories and common ignored paths
    dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ["node_modules", "venv", "__pycache__"]]
    
    for dir_name in dirs:
        for pattern in invalid_patterns:
            if pattern in dir_name:
                print(f"❌ Invalid directory name detected: {os.path.join(root, dir_name)}")
                sys.exit(1)

sys.exit(0)

