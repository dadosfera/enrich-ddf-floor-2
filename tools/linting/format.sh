#!/bin/bash
# Auto-formatting Script for Enrich DDF Floor 2
# Automatically fixes code style issues

set -e  # Exit on any error

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
LINTING_DIR="${PROJECT_ROOT}/tools/linting"

echo -e "${BLUE}🔧 Starting Auto-formatting Suite${NC}"
echo "Project Root: ${PROJECT_ROOT}"
echo "==============================================="

# Change to project root
cd "${PROJECT_ROOT}"

# Function to run a formatting tool
run_formatter() {
    local tool_name="$1"
    local command="$2"
    local description="$3"
    
    echo -e "\n${YELLOW}🔨 Running ${tool_name}...${NC}"
    echo "Description: ${description}"
    echo "Command: ${command}"
    echo "---"
    
    if eval "${command}"; then
        echo -e "${GREEN}✅ ${tool_name} completed${NC}"
        return 0
    else
        echo -e "${RED}❌ ${tool_name} failed${NC}"
        return 1
    fi
}

# 1. Remove unused imports and variables with autoflake (if available)
if command -v autoflake &> /dev/null; then
    run_formatter "autoflake" \
        "poetry run autoflake --in-place --remove-all-unused-imports --remove-unused-variables --recursive app/" \
        "Remove unused imports and variables"
fi

# 2. Sort imports with isort
run_formatter "isort" \
    "poetry run isort --settings-path=${LINTING_DIR}/pyproject.toml app/" \
    "Sort imports according to PEP8 and Black compatibility"

# 3. Format code with Black
run_formatter "Black" \
    "poetry run black --config=${LINTING_DIR}/pyproject.toml app/" \
    "Format code according to Black standards"

# 4. Remove trailing whitespace
echo -e "\n${YELLOW}🔨 Removing trailing whitespace...${NC}"
find app/ -name "*.py" -type f -exec sed -i '' 's/[[:space:]]*$//' {} +
echo -e "${GREEN}✅ Trailing whitespace removed${NC}"

# 5. Fix common issues with autopep8 (if available)
if command -v autopep8 &> /dev/null; then
    run_formatter "autopep8" \
        "poetry run autopep8 --in-place --aggressive --aggressive --recursive app/" \
        "Fix PEP8 style issues"
fi

echo -e "\n${GREEN}🎉 Auto-formatting completed!${NC}"
echo "Run './tools/linting/lint.sh' to verify code quality." 