#!/bin/bash

# Enrich DDF Floor 2 - Central Test Runner
# Version: 1.0.0
# Purpose: Centralized test execution with comprehensive coverage

set -euo pipefail

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Default values
TEST_TYPE="all"
VERBOSE=false
COVERAGE=false
FAIL_FAST=false
PARALLEL=false
TIMEOUT=300

# Help function
show_help() {
    cat << EOF
Enrich DDF Floor 2 - Test Runner

Usage: bash tests/run_tests.sh [OPTIONS]

OPTIONS:
    --all                    Run all tests (default)
    --unit                   Run unit tests only
    --integration            Run integration tests only
    --e2e                    Run end-to-end tests only
    --critical               Run critical path tests only
    --mutation               Run mutation tests only
    --coverage               Generate coverage report
    --verbose                Enable verbose output
    --fail-fast              Stop on first failure
    --parallel               Run tests in parallel
    --timeout=SECONDS        Test timeout (default: 300)
    --help                   Show this help message

EXAMPLES:
    # Run all tests with coverage
    bash tests/run_tests.sh --all --coverage --verbose

    # Run only unit tests
    bash tests/run_tests.sh --unit --fail-fast

    # Run critical tests with parallel execution
    bash tests/run_tests.sh --critical --parallel --timeout=600

    # Run E2E tests with verbose output
    bash tests/run_tests.sh --e2e --verbose
EOF
}

# Parse command line arguments
parse_args() {
    for arg in "$@"; do
        case $arg in
            --all)
                TEST_TYPE="all"
                shift
                ;;
            --unit)
                TEST_TYPE="unit"
                shift
                ;;
            --integration)
                TEST_TYPE="integration"
                shift
                ;;
            --e2e)
                TEST_TYPE="e2e"
                shift
                ;;
            --critical)
                TEST_TYPE="critical"
                shift
                ;;
            --mutation)
                TEST_TYPE="mutation"
                shift
                ;;
            --coverage)
                COVERAGE=true
                shift
                ;;
            --verbose)
                VERBOSE=true
                shift
                ;;
            --fail-fast)
                FAIL_FAST=true
                shift
                ;;
            --parallel)
                PARALLEL=true
                shift
                ;;
            --timeout=*)
                TIMEOUT="${arg#*=}"
                shift
                ;;
            --help)
                show_help
                exit 0
                ;;
            *)
                log_error "Unknown option: $arg"
                show_help
                exit 1
                ;;
        esac
    done
}

# Check dependencies
check_dependencies() {
    log_info "Checking test dependencies..."
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        log_error "Python 3 is required but not installed"
        exit 1
    fi
    
    # Check virtual environment
    if [[ ! -d "venv" ]]; then
        log_error "Virtual environment not found. Please run: python3 -m venv venv"
        exit 1
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Check pytest
    if ! python3 -c "import pytest" 2>/dev/null; then
        log_error "pytest is required but not installed"
        exit 1
    fi
    
    log_success "Dependencies check completed"
}

# Build pytest arguments
build_pytest_args() {
    local args=()
    
    # Test path based on type
    case $TEST_TYPE in
        all)
            args+=("tests/")
            ;;
        unit)
            args+=("tests/unit/")
            ;;
        integration)
            args+=("tests/integration/")
            ;;
        e2e)
            args+=("tests/e2e/")
            ;;
        critical)
            args+=("tests/unit/test_critical_endpoints.py" "tests/integration/test_critical_workflows.py" "tests/e2e/test_critical_scenarios.py")
            ;;
        mutation)
            args+=("tests/unit/test_mutation_tests.py")
            ;;
    esac
    
    # Add common options
    if [[ "$VERBOSE" == "true" ]]; then
        args+=("-v")
    fi
    
    if [[ "$FAIL_FAST" == "true" ]]; then
        args+=("-x")
    fi
    
    if [[ "$PARALLEL" == "true" ]]; then
        args+=("-n" "auto")
    fi
    
    if [[ "$COVERAGE" == "true" ]]; then
        args+=("--cov=." "--cov-report=html" "--cov-report=term-missing")
    fi
    
    # Add timeout
    args+=("--timeout=$TIMEOUT")
    
    echo "${args[@]}"
}

# Run tests
run_tests() {
    log_info "Running $TEST_TYPE tests..."
    
    source venv/bin/activate
    
    # Build pytest arguments
    local pytest_args=($(build_pytest_args))
    
    log_info "pytest arguments: ${pytest_args[*]}"
    
    # Run tests with timeout
    if timeout $((TIMEOUT + 30)) pytest "${pytest_args[@]}"; then
        log_success "All $TEST_TYPE tests passed"
        return 0
    else
        log_error "$TEST_TYPE tests failed"
        return 1
    fi
}

# Run pre-commit checks
run_pre_commit() {
    log_info "Running pre-commit checks..."
    
    source venv/bin/activate
    
    # Check if pre-commit is available
    if command -v pre-commit &> /dev/null; then
        if timeout 60 pre-commit run --all-files; then
            log_success "Pre-commit checks passed"
            return 0
        else
            log_error "Pre-commit checks failed"
            return 1
        fi
    else
        log_warning "pre-commit not found, skipping pre-commit checks"
        return 0
    fi
}

# Run linter checks
run_linters() {
    log_info "Running linter checks..."
    
    source venv/bin/activate
    
    local linter_failed=false
    
    # Run ruff
    if timeout 30 ruff check .; then
        log_success "Ruff checks passed"
    else
        log_error "Ruff checks failed"
        linter_failed=true
    fi
    
    # Run black check
    if timeout 30 black --check .; then
        log_success "Black formatting check passed"
    else
        log_error "Black formatting check failed"
        linter_failed=true
    fi
    
    # Run isort check
    if timeout 30 isort --check-only .; then
        log_success "Import sorting check passed"
    else
        log_error "Import sorting check failed"
        linter_failed=true
    fi
    
    # Run mypy
    if timeout 60 mypy .; then
        log_success "Type checking passed"
    else
        log_error "Type checking failed"
        linter_failed=true
    fi
    
    if [[ "$linter_failed" == "true" ]]; then
        return 1
    else
        return 0
    fi
}

# Generate test report
generate_report() {
    log_info "Generating test report..."
    
    local report_file="test_report_$(date +%Y%m%d_%H%M%S).txt"
    
    {
        echo "Enrich DDF Floor 2 - Test Report"
        echo "Generated: $(date)"
        echo "Test Type: $TEST_TYPE"
        echo "Coverage: $COVERAGE"
        echo "Verbose: $VERBOSE"
        echo "Fail Fast: $FAIL_FAST"
        echo "Parallel: $PARALLEL"
        echo "Timeout: $TIMEOUT seconds"
        echo ""
        echo "Test Results:"
        echo "============="
        
        if [[ "$COVERAGE" == "true" ]]; then
            echo "Coverage report available in: htmlcov/index.html"
        fi
        
        echo ""
        echo "Linter Results:"
        echo "==============="
        # Add linter results here if needed
        
    } > "$report_file"
    
    log_success "Test report generated: $report_file"
}

# Main execution function
main() {
    log_info "🧪 Starting Enrich DDF Floor 2 Test Runner"
    log_info "Version: 1.0.0"
    
    # Parse arguments
    parse_args "$@"
    
    # Check dependencies
    check_dependencies
    
    # Run pre-commit checks
    if ! run_pre_commit; then
        log_error "Pre-commit checks failed, aborting test run"
        exit 1
    fi
    
    # Run linter checks
    if ! run_linters; then
        log_error "Linter checks failed, aborting test run"
        exit 1
    fi
    
    # Run tests
    if run_tests; then
        log_success "Test execution completed successfully"
        
        # Generate report if requested
        if [[ "$COVERAGE" == "true" ]]; then
            generate_report
        fi
        
        exit 0
    else
        log_error "Test execution failed"
        exit 1
    fi
}

# Execute main function with all arguments
main "$@" 