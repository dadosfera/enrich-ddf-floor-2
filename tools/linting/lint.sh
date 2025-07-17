#!/bin/bash
# Professional Linting Script for Enrich DDF Floor 2
# Runs all linting tools in the correct order

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
LINTING_DIR="${PROJECT_ROOT}/tools/linting"
APP_DIR="${PROJECT_ROOT}/app"

echo -e "${BLUE}🔍 Starting Professional Linting Suite${NC}"
echo "Project Root: ${PROJECT_ROOT}"
echo "==============================================="

# Change to project root
cd "${PROJECT_ROOT}"

# Function to run a linting tool
run_linter() {
    local tool_name="$1"
    local command="$2"
    local description="$3"
    
    echo -e "\n${YELLOW}📋 Running ${tool_name}...${NC}"
    echo "Description: ${description}"
    echo "Command: ${command}"
    echo "---"
    
    if eval "${command}"; then
        echo -e "${GREEN}✅ ${tool_name} passed${NC}"
        return 0
    else
        echo -e "${RED}❌ ${tool_name} failed${NC}"
        return 1
    fi
}

# Function to check if tool is available
check_tool() {
    local tool="$1"
    if ! command -v "${tool}" &> /dev/null; then
        echo -e "${RED}❌ ${tool} is not installed${NC}"
        echo "Install with: poetry add --group dev ${tool}"
        return 1
    fi
    return 0
}

# Check required tools
echo -e "${BLUE}🔧 Checking required tools...${NC}"
TOOLS_OK=true

for tool in black isort flake8 mypy; do
    if ! check_tool "${tool}"; then
        TOOLS_OK=false
    fi
done

if [ "${TOOLS_OK}" = false ]; then
    echo -e "${RED}❌ Some tools are missing. Please install them first.${NC}"
    echo "Run: poetry install --with dev"
    exit 1
fi

echo -e "${GREEN}✅ All tools are available${NC}"

# Initialize counters
PASSED=0
FAILED=0
TOTAL=0

# 1. Import sorting with isort
TOTAL=$((TOTAL + 1))
if run_linter "isort" \
    "poetry run isort --settings-path=${LINTING_DIR}/pyproject.toml --check-only --diff app/" \
    "Sort imports according to PEP8 and Black compatibility"; then
    PASSED=$((PASSED + 1))
else
    FAILED=$((FAILED + 1))
    echo "💡 To fix: poetry run isort --settings-path=${LINTING_DIR}/pyproject.toml app/"
fi

# 2. Code formatting with Black
TOTAL=$((TOTAL + 1))
if run_linter "Black" \
    "poetry run black --config=${LINTING_DIR}/pyproject.toml --check --diff app/" \
    "Code formatting according to Black standards"; then
    PASSED=$((PASSED + 1))
else
    FAILED=$((FAILED + 1))
    echo "💡 To fix: poetry run black --config=${LINTING_DIR}/pyproject.toml app/"
fi

# 3. Linting with flake8
TOTAL=$((TOTAL + 1))
if run_linter "flake8" \
    "poetry run flake8 --config=${LINTING_DIR}/.flake8 app/" \
    "Code quality and style checking"; then
    PASSED=$((PASSED + 1))
else
    FAILED=$((FAILED + 1))
fi

# 4. Type checking with mypy
TOTAL=$((TOTAL + 1))
if run_linter "mypy" \
    "poetry run mypy --config-file=${LINTING_DIR}/pyproject.toml app/" \
    "Static type checking"; then
    PASSED=$((PASSED + 1))
else
    FAILED=$((FAILED + 1))
fi

# 5. Security check with bandit (if available)
if command -v bandit &> /dev/null; then
    TOTAL=$((TOTAL + 1))
    if run_linter "bandit" \
        "poetry run bandit -r app/ -x tests/" \
        "Security vulnerability scanning"; then
        PASSED=$((PASSED + 1))
    else
        FAILED=$((FAILED + 1))
    fi
fi

# Summary
echo -e "\n${BLUE}📊 Linting Summary${NC}"
echo "==============================================="
echo -e "Total checks: ${TOTAL}"
echo -e "Passed: ${GREEN}${PASSED}${NC}"
echo -e "Failed: ${RED}${FAILED}${NC}"

if [ "${FAILED}" -eq 0 ]; then
    echo -e "\n${GREEN}🎉 All linting checks passed!${NC}"
    echo "Code quality is excellent ✨"
    exit 0
else
    echo -e "\n${RED}❌ ${FAILED} linting check(s) failed${NC}"
    echo "Please fix the issues above before committing."
    exit 1
fi 