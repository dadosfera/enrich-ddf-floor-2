#!/bin/bash
# Comprehensive Test Runner Script
# Enrich DDF Floor 2 - Automated testing suite execution

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

# Configuration
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
REPORTS_DIR="${PROJECT_ROOT}/test-reports"
COVERAGE_DIR="${REPORTS_DIR}/coverage"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

cd "${PROJECT_ROOT}"

# Function to display usage
usage() {
    echo -e "${BLUE}Comprehensive Test Runner${NC}"
    echo "Usage: $0 [OPTIONS] [TEST_TYPE]"
    echo ""
    echo "Test Types:"
    echo "  unit        - Run unit tests only"
    echo "  integration - Run integration tests only"
    echo "  api         - Run API tests only"
    echo "  coverage    - Run tests with coverage analysis"
    echo "  lint        - Run code quality checks"
    echo "  security    - Run security tests"
    echo "  all         - Run all tests (default)"
    echo ""
    echo "Options:"
    echo "  -v, --verbose    Verbose output"
    echo "  -f, --fast       Skip slow tests"
    echo "  -c, --clean      Clean previous test artifacts"
    echo "  -r, --report     Generate detailed reports"
    echo "  -h, --help       Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 unit                    # Run unit tests"
    echo "  $0 all --report           # Run all tests with reports"
    echo "  $0 coverage --verbose     # Run coverage analysis with verbose output"
    echo ""
}

# Function to log different types of messages
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

log_step() {
    echo -e "${CYAN}📋 $1${NC}"
}

log_section() {
    echo -e "${MAGENTA}🔍 $1${NC}"
    echo "$(printf '%*s' ${#1} | tr ' ' '=')"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to setup test environment
setup_test_environment() {
    log_step "Setting up test environment..."
    
    # Create reports directory
    mkdir -p "$REPORTS_DIR"
    mkdir -p "$COVERAGE_DIR"
    
    # Check if Poetry is available
    if ! command_exists poetry; then
        log_error "Poetry not found. Please install Poetry first."
        exit 1
    fi
    
    # Check if development dependencies are installed
    if ! poetry show pytest > /dev/null 2>&1; then
        log_warning "Test dependencies not found. Installing..."
        poetry install --with dev
    fi
    
    # Set test environment variables
    export TESTING=true
    export DATABASE_URL="sqlite+aiosqlite:///./test.db"
    export REDIS_URL="redis://localhost:6379/15"  # Use different Redis DB for tests
    
    log_success "Test environment ready"
}

# Function to clean test artifacts
clean_test_artifacts() {
    log_step "Cleaning previous test artifacts..."
    
    # Remove test databases
    rm -f test.db test.db-*
    
    # Clean pytest cache
    rm -rf .pytest_cache
    
    # Clean coverage files
    rm -f .coverage .coverage.*
    
    # Clean test reports (but keep directory)
    if [ -d "$REPORTS_DIR" ]; then
        find "$REPORTS_DIR" -type f -name "*.xml" -o -name "*.html" -o -name "*.json" | xargs rm -f
    fi
    
    log_success "Test artifacts cleaned"
}

# Function to run unit tests
run_unit_tests() {
    log_section "Running Unit Tests"
    
    local pytest_args=()
    
    # Add verbose flag if requested
    if [ "$VERBOSE" = true ]; then
        pytest_args+=("-v")
    fi
    
    # Add fast flag if requested
    if [ "$FAST" = true ]; then
        pytest_args+=("-m" "not slow")
    fi
    
    # Add report generation if requested
    if [ "$GENERATE_REPORTS" = true ]; then
        pytest_args+=("--junitxml=${REPORTS_DIR}/unit-tests.xml")
    fi
    
    # Run unit tests
    if poetry run pytest tests/unit/ "${pytest_args[@]}" 2>/dev/null; then
        log_success "Unit tests passed"
        return 0
    else
        log_error "Unit tests failed"
        return 1
    fi
}

# Function to run integration tests
run_integration_tests() {
    log_section "Running Integration Tests"
    
    # Check if database is available for integration tests
    if ! tools/database/health-check.sh > /dev/null 2>&1; then
        log_warning "Database not available for integration tests"
        return 1
    fi
    
    local pytest_args=()
    
    if [ "$VERBOSE" = true ]; then
        pytest_args+=("-v")
    fi
    
    if [ "$FAST" = true ]; then
        pytest_args+=("-m" "not slow")
    fi
    
    if [ "$GENERATE_REPORTS" = true ]; then
        pytest_args+=("--junitxml=${REPORTS_DIR}/integration-tests.xml")
    fi
    
    # Run integration tests
    if poetry run pytest tests/integration/ "${pytest_args[@]}" 2>/dev/null; then
        log_success "Integration tests passed"
        return 0
    else
        log_error "Integration tests failed"
        return 1
    fi
}

# Function to run API tests
run_api_tests() {
    log_section "Running API Tests"
    
    local pytest_args=()
    
    if [ "$VERBOSE" = true ]; then
        pytest_args+=("-v")
    fi
    
    if [ "$GENERATE_REPORTS" = true ]; then
        pytest_args+=("--junitxml=${REPORTS_DIR}/api-tests.xml")
    fi
    
    # Run API tests
    if poetry run pytest tests/api/ "${pytest_args[@]}" 2>/dev/null; then
        log_success "API tests passed"
        return 0
    else
        log_error "API tests failed"
        return 1
    fi
}

# Function to run coverage analysis
run_coverage_tests() {
    log_section "Running Coverage Analysis"
    
    local pytest_args=(
        "--cov=app"
        "--cov-report=term-missing"
        "--cov-report=html:${COVERAGE_DIR}"
        "--cov-fail-under=80"
    )
    
    if [ "$VERBOSE" = true ]; then
        pytest_args+=("-v")
    fi
    
    if [ "$GENERATE_REPORTS" = true ]; then
        pytest_args+=("--cov-report=xml:${REPORTS_DIR}/coverage.xml")
        pytest_args+=("--junitxml=${REPORTS_DIR}/coverage-tests.xml")
    fi
    
    # Run tests with coverage
    if poetry run pytest tests/ "${pytest_args[@]}"; then
        log_success "Coverage analysis completed"
        
        # Display coverage summary
        echo ""
        log_info "Coverage Report Summary:"
        poetry run coverage report --show-missing | tail -n 10
        
        if [ "$GENERATE_REPORTS" = true ]; then
            log_info "Detailed coverage report: ${COVERAGE_DIR}/index.html"
        fi
        
        return 0
    else
        log_error "Coverage analysis failed (coverage below threshold)"
        return 1
    fi
}

# Function to run linting tests
run_lint_tests() {
    log_section "Running Code Quality Checks"
    
    if [ -f "tools/linting/lint.sh" ]; then
        if ./tools/linting/lint.sh; then
            log_success "Code quality checks passed"
            return 0
        else
            log_error "Code quality checks failed"
            return 1
        fi
    else
        log_warning "Linting tools not found"
        return 1
    fi
}

# Function to run security tests
run_security_tests() {
    log_section "Running Security Tests"
    
    local security_status=0
    
    # Run bandit security scan
    if command_exists bandit; then
        log_step "Running Bandit security scan..."
        
        if poetry run bandit -r app/ -f json -o "${REPORTS_DIR}/security-report.json" 2>/dev/null; then
            log_success "Security scan completed"
        else
            log_error "Security vulnerabilities found"
            security_status=1
        fi
    else
        log_warning "Bandit not available for security scanning"
    fi
    
    # Run safety check for dependencies
    if command_exists safety; then
        log_step "Running dependency security check..."
        
        if poetry run safety check --json --output "${REPORTS_DIR}/safety-report.json" 2>/dev/null; then
            log_success "Dependency security check passed"
        else
            log_error "Vulnerable dependencies found"
            security_status=1
        fi
    else
        log_warning "Safety not available for dependency checking"
    fi
    
    return $security_status
}

# Function to generate test summary
generate_test_summary() {
    log_section "Test Summary"
    
    local summary_file="${REPORTS_DIR}/test-summary-${TIMESTAMP}.txt"
    
    {
        echo "Test Execution Summary"
        echo "====================="
        echo "Timestamp: $(date)"
        echo "Test Type: $TEST_TYPE"
        echo "Options: Verbose=$VERBOSE, Fast=$FAST, Reports=$GENERATE_REPORTS"
        echo ""
        echo "Results:"
        echo "--------"
        
        for result in "${TEST_RESULTS[@]}"; do
            echo "$result"
        done
        
        echo ""
        echo "Total Tests: ${#TEST_RESULTS[@]}"
        echo "Passed: $TESTS_PASSED"
        echo "Failed: $TESTS_FAILED"
        
        if [ $TESTS_FAILED -eq 0 ]; then
            echo "Overall Status: PASSED"
        else
            echo "Overall Status: FAILED"
        fi
        
    } | tee "$summary_file"
    
    if [ "$GENERATE_REPORTS" = true ]; then
        log_info "Test summary saved: $summary_file"
    fi
}

# Parse command line arguments
VERBOSE=false
FAST=false
CLEAN=false
GENERATE_REPORTS=false
TEST_TYPE="all"

while [[ $# -gt 0 ]]; do
    case $1 in
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -f|--fast)
            FAST=true
            shift
            ;;
        -c|--clean)
            CLEAN=true
            shift
            ;;
        -r|--report)
            GENERATE_REPORTS=true
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        unit|integration|api|coverage|lint|security|all)
            TEST_TYPE=$1
            shift
            ;;
        *)
            log_error "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

# Main execution
echo -e "${BLUE}🧪 Comprehensive Test Runner - Enrich DDF Floor 2${NC}"
echo "=================================================="
echo "Test Type: $TEST_TYPE"
echo "Timestamp: $(date)"
echo ""

# Initialize counters
TEST_RESULTS=()
TESTS_PASSED=0
TESTS_FAILED=0

# Clean artifacts if requested
if [ "$CLEAN" = true ]; then
    clean_test_artifacts
fi

# Setup test environment
setup_test_environment

# Run tests based on type
case $TEST_TYPE in
    unit)
        if run_unit_tests; then
            TEST_RESULTS+=("Unit Tests: PASSED")
            TESTS_PASSED=$((TESTS_PASSED + 1))
        else
            TEST_RESULTS+=("Unit Tests: FAILED")
            TESTS_FAILED=$((TESTS_FAILED + 1))
        fi
        ;;
    integration)
        if run_integration_tests; then
            TEST_RESULTS+=("Integration Tests: PASSED")
            TESTS_PASSED=$((TESTS_PASSED + 1))
        else
            TEST_RESULTS+=("Integration Tests: FAILED")
            TESTS_FAILED=$((TESTS_FAILED + 1))
        fi
        ;;
    api)
        if run_api_tests; then
            TEST_RESULTS+=("API Tests: PASSED")
            TESTS_PASSED=$((TESTS_PASSED + 1))
        else
            TEST_RESULTS+=("API Tests: FAILED")
            TESTS_FAILED=$((TESTS_FAILED + 1))
        fi
        ;;
    coverage)
        if run_coverage_tests; then
            TEST_RESULTS+=("Coverage Analysis: PASSED")
            TESTS_PASSED=$((TESTS_PASSED + 1))
        else
            TEST_RESULTS+=("Coverage Analysis: FAILED")
            TESTS_FAILED=$((TESTS_FAILED + 1))
        fi
        ;;
    lint)
        if run_lint_tests; then
            TEST_RESULTS+=("Code Quality: PASSED")
            TESTS_PASSED=$((TESTS_PASSED + 1))
        else
            TEST_RESULTS+=("Code Quality: FAILED")
            TESTS_FAILED=$((TESTS_FAILED + 1))
        fi
        ;;
    security)
        if run_security_tests; then
            TEST_RESULTS+=("Security Tests: PASSED")
            TESTS_PASSED=$((TESTS_PASSED + 1))
        else
            TEST_RESULTS+=("Security Tests: FAILED")
            TESTS_FAILED=$((TESTS_FAILED + 1))
        fi
        ;;
    all)
        # Run all test types
        for test_type in unit integration api coverage lint security; do
            case $test_type in
                unit)
                    if run_unit_tests; then
                        TEST_RESULTS+=("Unit Tests: PASSED")
                        TESTS_PASSED=$((TESTS_PASSED + 1))
                    else
                        TEST_RESULTS+=("Unit Tests: FAILED")
                        TESTS_FAILED=$((TESTS_FAILED + 1))
                    fi
                    ;;
                integration)
                    if run_integration_tests; then
                        TEST_RESULTS+=("Integration Tests: PASSED")
                        TESTS_PASSED=$((TESTS_PASSED + 1))
                    else
                        TEST_RESULTS+=("Integration Tests: FAILED")
                        TESTS_FAILED=$((TESTS_FAILED + 1))
                    fi
                    ;;
                api)
                    if run_api_tests; then
                        TEST_RESULTS+=("API Tests: PASSED")
                        TESTS_PASSED=$((TESTS_PASSED + 1))
                    else
                        TEST_RESULTS+=("API Tests: FAILED")
                        TESTS_FAILED=$((TESTS_FAILED + 1))
                    fi
                    ;;
                coverage)
                    if run_coverage_tests; then
                        TEST_RESULTS+=("Coverage Analysis: PASSED")
                        TESTS_PASSED=$((TESTS_PASSED + 1))
                    else
                        TEST_RESULTS+=("Coverage Analysis: FAILED")
                        TESTS_FAILED=$((TESTS_FAILED + 1))
                    fi
                    ;;
                lint)
                    if run_lint_tests; then
                        TEST_RESULTS+=("Code Quality: PASSED")
                        TESTS_PASSED=$((TESTS_PASSED + 1))
                    else
                        TEST_RESULTS+=("Code Quality: FAILED")
                        TESTS_FAILED=$((TESTS_FAILED + 1))
                    fi
                    ;;
                security)
                    if run_security_tests; then
                        TEST_RESULTS+=("Security Tests: PASSED")
                        TESTS_PASSED=$((TESTS_PASSED + 1))
                    else
                        TEST_RESULTS+=("Security Tests: FAILED")
                        TESTS_FAILED=$((TESTS_FAILED + 1))
                    fi
                    ;;
            esac
            echo ""  # Add spacing between test types
        done
        ;;
esac

# Generate summary
generate_test_summary

# Exit with appropriate code
if [ $TESTS_FAILED -eq 0 ]; then
    echo ""
    log_success "All tests passed successfully! 🎉"
    exit 0
else
    echo ""
    log_error "Some tests failed. Please review the results above."
    exit 1
fi 