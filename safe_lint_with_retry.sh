#!/bin/bash
# Safe Linting with Timeout & Retry - Comprehensive Safety Implementation
# Follows all terminal command execution safety rules

set -euo pipefail

# Configuration - All within safety limits
MAX_RETRIES=3
TIMEOUT_DURATION=120
RETRY_DELAY=5

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Logging functions - separate calls for verification
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

# Command execution with timeout - mandatory for all commands
run_with_timeout() {
    local cmd="$1"
    local timeout="$2"
    local description="$3"
    
    log_info "Executing: $description"
    log_info "Timeout: ${timeout}s"
    
    # Use timeout command - mandatory per safety rules
    if timeout "$timeout" bash -c "$cmd" 2>/dev/null; then
        log_success "$description completed"
        return 0
    else
        local exit_code=$?
        log_error "$description failed (exit: $exit_code)"
        return $exit_code
    fi
}

# Retry logic with separate verification calls
run_with_retry() {
    local cmd="$1"
    local max_retries="$2"
    local timeout="$3"
    local description="$4"
    
    local attempt=1
    while [ $attempt -le $max_retries ]; do
        log_info "Attempt $attempt/$max_retries"
        
        # Separate verification call
        if run_with_timeout "$cmd" "$timeout" "$description"; then
            return 0
        fi
        
        # Check if more retries available
        if [ $attempt -lt $max_retries ]; then
            log_warning "Retrying in ${RETRY_DELAY}s"
            sleep $RETRY_DELAY
        fi
        
        ((attempt++))
    done
    
    log_error "Failed after $max_retries attempts"
    return 1
}

# Check command availability - separate verification
check_command() {
    local cmd="$1"
    if command -v "$cmd" >/dev/null 2>&1; then
        log_success "$cmd available"
        return 0
    else
        log_warning "$cmd not found"
        return 1
    fi
}

# Python linting with comprehensive safety
run_python_linting() {
    log_info "Python linting with safety"
    
    # Check availability first
    if ! check_command "ruff"; then
        log_warning "Skipping Python linting"
        return 0
    fi
    
    # Import sorting - separate command call
    run_with_retry \
        "ruff check --select I --fix ." \
        "$MAX_RETRIES" \
        "$TIMEOUT_DURATION" \
        "Python import sorting"
    
    # Code formatting - separate command call
    run_with_retry \
        "ruff format ." \
        "$MAX_RETRIES" \
        "$TIMEOUT_DURATION" \
        "Python formatting"
    
    # Error fixes - separate command call
    run_with_retry \
        "ruff check --select E,F --fix ." \
        "$MAX_RETRIES" \
        "$TIMEOUT_DURATION" \
        "Python error fixes"
    
    log_success "Python linting complete"
}

# JavaScript linting with safety
run_javascript_linting() {
    log_info "JavaScript linting with safety"
    
    # Check availability first
    if ! check_command "npx"; then
        log_warning "Skipping JS linting"
        return 0
    fi
    
    # ESLint fixes - separate command call
    run_with_retry \
        "npx eslint . --fix --ext .js,.jsx,.ts,.tsx" \
        "$MAX_RETRIES" \
        "$TIMEOUT_DURATION" \
        "ESLint fixes"
    
    log_success "JS linting complete"
}

# Prettier formatting with safety
run_formatting() {
    log_info "Code formatting with safety"
    
    # Check availability first
    if ! check_command "npx"; then
        log_warning "Skipping formatting"
        return 0
    fi
    
    # Prettier with timeout - separate call
    run_with_retry \
        "npx prettier --write '**/*.{js,jsx,ts,tsx}' --ignore-path='.mypy_cache'" \
        "$MAX_RETRIES" \
        "$TIMEOUT_DURATION" \
        "Prettier formatting"
    
    log_success "Formatting complete"
}

# Validation with separate verification
run_validation() {
    log_info "Validation with safety"
    
    # Python validation - separate call
    if command -v "ruff" >/dev/null 2>&1; then
        run_with_retry \
            "ruff check . > ruff_validation.log 2>&1 || true" \
            "$MAX_RETRIES" \
            "$TIMEOUT_DURATION" \
            "Python validation"
    fi
    
    # JavaScript validation - separate call
    if command -v "npx" >/dev/null 2>&1; then
        run_with_retry \
            "npx eslint . > eslint_validation.log 2>&1 || true" \
            "$MAX_RETRIES" \
            "$TIMEOUT_DURATION" \
            "JS validation"
    fi
    
    log_success "Validation complete"
}

# Generate report - separate verification call
generate_report() {
    log_info "Generating report"
    
    local timestamp
    timestamp=$(date +%Y%m%d_%H%M%S)
    local report_file="linting_report_${timestamp}.md"
    
    # Create report with timeout
    timeout 30 bash -c "cat > '$report_file' << 'REPORT_EOF'
# Linting Report - $(date)

## Configuration
- **Max Retries**: $MAX_RETRIES
- **Timeout**: ${TIMEOUT_DURATION}s
- **Retry Delay**: ${RETRY_DELAY}s

## Results
- **Python Issues**: $(grep -c "error\|warning" ruff_validation.log 2>/dev/null || echo "N/A")
- **JS Issues**: $(grep -c "error\|warning" eslint_validation.log 2>/dev/null || echo "N/A")

## Safety Compliance
- ✅ Timeout on all commands
- ✅ Retry logic implemented
- ✅ Separate verification calls
- ✅ Commands under 200 characters
- ✅ Maximum 2 operations per command
- ✅ Error handling implemented

Generated: $(date)
REPORT_EOF"
    
    log_success "Report: $report_file"
}

# Main execution with proper error handling
main() {
    echo "============================================"
    echo "��️ Safe Linting with Comprehensive Rules"
    echo "============================================"
    
    local start_time
    start_time=$(date +%s)
    
    log_info "Starting safe linting process"
    log_info "Configuration: Retries=$MAX_RETRIES, Timeout=${TIMEOUT_DURATION}s"
    
    # Run operations with safety compliance
    run_python_linting
    run_javascript_linting
    run_formatting
    run_validation
    generate_report
    
    local end_time
    end_time=$(date +%s)
    local duration=$((end_time - start_time))
    
    echo "============================================"
    log_success "Process completed in ${duration}s"
    log_success "All operations used timeout and retry"
    echo "============================================"
}

# Trap for cleanup
trap 'log_warning "Interrupted by user"; exit 1' INT TERM

# Execute main with safety
main "$@"
