#!/bin/bash

# Enrich DDF Floor 2 - Main Application Entry Point
# Version: 1.0.0
# Purpose: Centralized application execution with platform-specific handling

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
PLATFORM="local-macos"
ENVIRONMENT="dev"
TOLERANT=false
VERBOSE=false
DEBUG=false
FULL=false
TEST=false
PORT=""
HOST="0.0.0.0"
START_TIMEOUT=0

# Help function
show_help() {
    cat << EOF
Enrich DDF Floor 2 - Application Runner

Usage: bash workflows/run.sh [OPTIONS]

OPTIONS:
    --platform=PLATFORM     Target platform (default: local-macos)
                           Options: local-macos, local-linux, docker, kubernetes
    --env=ENVIRONMENT      Environment (default: dev)
                           Options: dev, staging, production
    --tolerant             Continue on non-critical errors
    --verbose              Enable verbose output
    --debug                Enable debug mode
    --full                 Full deployment mode
    --test                 Run tests only
    --port=PORT           Custom port (default: auto-detect)
    --host=HOST           Custom host (default: 0.0.0.0)
    --timeout=SECONDS     Optional startup timeout (0 = no timeout; default: 0)
    --help                 Show this help message

EXAMPLES:
    # Development mode
    bash workflows/run.sh --platform=local-macos --env=dev --verbose

    # Production mode
    bash workflows/run.sh --platform=docker --env=production --full

    # Test mode
    bash workflows/run.sh --test --verbose

    # Custom port
    bash workflows/run.sh --port=8080 --env=dev
EOF
}

# Parse command line arguments
parse_args() {
    for arg in "$@"; do
        case $arg in
            --platform=*)
                PLATFORM="${arg#*=}"
                shift
                ;;
            --env=*)
                ENVIRONMENT="${arg#*=}"
                shift
                ;;
            --tolerant)
                TOLERANT=true
                shift
                ;;
            --verbose)
                VERBOSE=true
                shift
                ;;
            --debug)
                DEBUG=true
                shift
                ;;
            --full)
                FULL=true
                shift
                ;;
            --test)
                TEST=true
                shift
                ;;
            --port=*)
                PORT="${arg#*=}"
                shift
                ;;
            --host=*)
                HOST="${arg#*=}"
                shift
                ;;
            --timeout=*)
                START_TIMEOUT="${arg#*=}"
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

# Validate platform
validate_platform() {
    case $PLATFORM in
        local-macos|local-linux|docker|kubernetes)
            log_info "Platform: $PLATFORM"
            ;;
        *)
            log_error "Invalid platform: $PLATFORM"
            exit 1
            ;;
    esac
}

# Validate environment
validate_environment() {
    case $ENVIRONMENT in
        dev|staging|production)
            log_info "Environment: $ENVIRONMENT"
            ;;
        *)
            log_error "Invalid environment: $ENVIRONMENT"
            exit 1
            ;;
    esac
}

# Check dependencies
check_dependencies() {
    log_info "Checking dependencies..."

    # Check Python
    if ! command -v python3 &> /dev/null; then
        log_error "Python 3 is required but not installed"
        exit 1
    fi

    # Check virtual environment
    if [[ ! -d "venv" ]]; then
        log_warning "Virtual environment not found, creating..."
        python3 -m venv venv
    fi

    # Activate virtual environment
    source venv/bin/activate

    # Check required packages
    if ! python3 -c "import fastapi, uvicorn, sqlalchemy" 2>/dev/null; then
        log_warning "Required packages not found, installing..."
        pip install -r requirements-minimal.txt
    fi

    log_success "Dependencies check completed"
}

# Find available port
find_available_port() {
    if [[ -n "$PORT" ]]; then
        echo "$PORT"
        return
    fi

    # Default port range
    local start_port=8000
    local end_port=9000

    for port in $(seq $start_port $end_port); do
        if ! timeout 1 bash -c "</dev/tcp/localhost/$port" 2>/dev/null; then
            echo "$port"
            return
        fi
    done

    log_error "No available ports found in range $start_port-$end_port"
    exit 1
}

# Run tests
run_tests() {
    log_info "Running test suite..."

    source venv/bin/activate

    # Run with timeout to prevent hanging
    if timeout 300 pytest -v --tb=short --cov=. --cov-report=html; then
        log_success "All tests passed"
        return 0
    else
        log_error "Tests failed"
        return 1
    fi
}

# Start application
start_application() {
    log_info "Starting application..."

    local app_port=$(find_available_port)
    log_info "Using port: $app_port"

    # Set environment variables
    export APP_PORT="$app_port"
    export APP_HOST="$HOST"
    export APP_ENV="$ENVIRONMENT"
    export APP_DEBUG="$DEBUG"
    # Also export standard variables consumed by pydantic-settings
    export PORT="$app_port"
    export HOST="$HOST"

    if [[ "$VERBOSE" == "true" ]]; then
        export APP_VERBOSE="true"
    fi

    source venv/bin/activate

    # Start application with optional timeout control
    if [[ "$START_TIMEOUT" -gt 0 ]]; then
        log_info "Applying startup timeout: ${START_TIMEOUT}s"
        if timeout "$START_TIMEOUT" python3 main.py; then
            log_success "Application exited successfully within timeout"
            return 0
        else
            log_error "Application failed or timed out during startup window"
            return 1
        fi
    else
        # No timeout; run in foreground to allow interactive dev
        python3 main.py
        local exit_code=$?
        if [[ $exit_code -eq 0 ]]; then
            log_success "Application exited successfully"
        else
            log_error "Application exited with code $exit_code"
        fi
        return $exit_code
    fi
}

# Platform-specific setup
setup_platform() {
    case $PLATFORM in
        local-macos)
            log_info "Setting up for macOS..."
            # macOS specific setup if needed
            ;;
        local-linux)
            log_info "Setting up for Linux..."
            # Linux specific setup if needed
            ;;
        docker)
            log_info "Setting up for Docker..."
            # Docker setup would go here
            log_warning "Docker setup not implemented yet"
            ;;
        kubernetes)
            log_info "Setting up for Kubernetes..."
            # Kubernetes setup would go here
            log_warning "Kubernetes setup not implemented yet"
            ;;
    esac
}

# Main execution function
main() {
    log_info "🚀 Starting Enrich DDF Floor 2 Application"
    log_info "Version: 1.0.0"

    # Parse arguments
    parse_args "$@"

    # Validate inputs
    validate_platform
    validate_environment

    # Setup platform
    setup_platform

    # Check dependencies
    check_dependencies

    # Execute based on mode
    if [[ "$TEST" == "true" ]]; then
        if run_tests; then
            log_success "Test execution completed successfully"
            exit 0
        else
            log_error "Test execution failed"
            exit 1
        fi
    else
        if start_application; then
            log_success "Application execution completed successfully"
            exit 0
        else
            log_error "Application execution failed"
            exit 1
        fi
    fi
}

# Execute main function with all arguments
main "$@"
