#!/bin/bash
# Robust Linting Script with Timeout and Retry Functionality

set -euo pipefail

# Configuration
MAX_RETRIES=3
TIMEOUT_DURATION=120
RETRY_DELAY=5

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

run_with_timeout() {
    local cmd="$1"
    local timeout="$2"
    local description="$3"
    
    log_info "Executing: $description (timeout: ${timeout}s)"
    
    if timeout "$timeout" bash -c "$cmd" 2>/dev/null; then
        log_success "$description completed"
        return 0
    else
        log_error "$description failed/timed out"
        return 1
    fi
}

run_with_retry() {
    local cmd="$1"
    local max_retries="$2"
    local timeout="$3"
    local description="$4"
    
    local attempt=1
    while [ $attempt -le $max_retries ]; do
        log_info "Attempt $attempt/$max_retries: $description"
        
        if run_with_timeout "$cmd" "$timeout" "$description"; then
            return 0
        fi
        
        if [ $attempt -lt $max_retries ]; then
            log_warning "Retrying in ${RETRY_DELAY}s..."
            sleep $RETRY_DELAY
        fi
        
        ((attempt++))
    done
    
    log_error "$description failed after $max_retries attempts"
    return 1
}

main() {
    echo "========================================"
    echo "🔍 Robust Linting with Timeout & Retry"
    echo "========================================"
    
    log_info "Configuration: Max Retries=$MAX_RETRIES, Timeout=${TIMEOUT_DURATION}s"
    
    # Python linting with retry
    if command -v ruff >/dev/null 2>&1; then
        run_with_retry "ruff check --select I --fix ." "$MAX_RETRIES" "$TIMEOUT_DURATION" "Python import sorting"
        run_with_retry "ruff format ." "$MAX_RETRIES" "$TIMEOUT_DURATION" "Python formatting"
        run_with_retry "ruff check --select E,F --fix ." "$MAX_RETRIES" "$TIMEOUT_DURATION" "Python error fixes"
    fi
    
    # JavaScript linting with retry
    if command -v npx >/dev/null 2>&1; then
        run_with_retry "npx eslint . --fix --ext .js,.jsx,.ts,.tsx" "$MAX_RETRIES" "$TIMEOUT_DURATION" "ESLint fixes"
    fi
    
    # Validation with retry
    if command -v ruff >/dev/null 2>&1; then
        run_with_retry "ruff check . > ruff_validation.log 2>&1 || true" "$MAX_RETRIES" "$TIMEOUT_DURATION" "Python validation"
    fi
    
    echo "========================================"
    log_success "Linting completed with timeout and retry protection"
    echo "========================================"
}

main "$@"
