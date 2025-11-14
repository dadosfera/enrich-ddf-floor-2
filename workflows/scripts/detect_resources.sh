#!/bin/bash

# Resource Detection and Adaptive Configuration Script
# Detects available CPU, RAM, and determines optimal parallelization settings
# Version: 1.0.0

set -euo pipefail

# Color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

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

# Detect OS
detect_os() {
    case "$(uname -s)" in
        Darwin*)
            echo "macos"
            ;;
        Linux*)
            echo "linux"
            ;;
        *)
            echo "unknown"
            ;;
    esac
}

# Get total CPU cores
get_cpu_cores() {
    local os=$(detect_os)
    case "$os" in
        macos)
            sysctl -n hw.ncpu
            ;;
        linux)
            nproc
            ;;
        *)
            echo "4"  # Default fallback
            ;;
    esac
}

# Get available CPU cores (accounting for load)
get_available_cpu_cores() {
    local total_cores=$(get_cpu_cores)
    local os=$(detect_os)

    case "$os" in
        macos)
            local load=$(sysctl -n vm.loadavg | awk '{print $2}')
            ;;
        linux)
            local load=$(cat /proc/loadavg | awk '{print $1}')
            ;;
        *)
            local load=0
            ;;
    esac

    # Calculate available cores (total - load, minimum 1)
    local available=$(echo "$total_cores - $load" | bc | awk '{print int($1+0.5)}')
    if [ "$available" -lt 1 ]; then
        available=1
    fi

    echo "$available"
}

# Get total RAM in GB
get_total_ram_gb() {
    local os=$(detect_os)
    case "$os" in
        macos)
            local bytes=$(sysctl -n hw.memsize)
            echo "scale=2; $bytes / 1024 / 1024 / 1024" | bc
            ;;
        linux)
            local kb=$(grep MemTotal /proc/meminfo | awk '{print $2}')
            echo "scale=2; $kb / 1024 / 1024" | bc
            ;;
        *)
            echo "8"  # Default fallback
            ;;
    esac
}

# Get available RAM in GB
get_available_ram_gb() {
    local os=$(detect_os)
    case "$os" in
        macos)
            local pages_free=$(vm_stat | grep "Pages free" | awk '{print $3}' | tr -d '.')
            local pages_inactive=$(vm_stat | grep "Pages inactive" | awk '{print $3}' | tr -d '.')
            local page_size=$(pagesize)
            local available_bytes=$(echo "($pages_free + $pages_inactive) * $page_size" | bc)
            echo "scale=2; $available_bytes / 1024 / 1024 / 1024" | bc
            ;;
        linux)
            local kb=$(grep MemAvailable /proc/meminfo | awk '{print $2}')
            echo "scale=2; $kb / 1024 / 1024" | bc
            ;;
        *)
            echo "4"  # Default fallback
            ;;
    esac
}

# Calculate optimal workers for Playwright
calculate_playwright_workers() {
    local available_cores=$1
    local available_ram_gb=$2
    local mode=${3:-"balanced"}

    # Playwright needs ~500MB per worker
    local max_workers_by_ram=$(echo "$available_ram_gb / 0.5" | bc | awk '{print int($1)}')

    case "$mode" in
        conservative)
            # Use 50% of available cores, capped by RAM
            local workers=$(echo "$available_cores * 0.5" | bc | awk '{print int($1+0.5)}')
            ;;
        balanced)
            # Use 75% of available cores, capped by RAM
            local workers=$(echo "$available_cores * 0.75" | bc | awk '{print int($1+0.5)}')
            ;;
        aggressive)
            # Use 100% of available cores, capped by RAM
            local workers=$available_cores
            ;;
        *)
            local workers=2
            ;;
    esac

    # Cap by RAM availability
    if [ "$workers" -gt "$max_workers_by_ram" ]; then
        workers=$max_workers_by_ram
    fi

    # Minimum 1, maximum 16
    if [ "$workers" -lt 1 ]; then
        workers=1
    elif [ "$workers" -gt 16 ]; then
        workers=16
    fi

    echo "$workers"
}

# Calculate optimal Node.js memory
calculate_node_memory() {
    local available_ram_gb=$1
    local mode=${2:-"balanced"}

    case "$mode" in
        conservative)
            # Use 25% of available RAM
            local memory=$(echo "$available_ram_gb * 0.25 * 1024" | bc | awk '{print int($1)}')
            ;;
        balanced)
            # Use 40% of available RAM
            local memory=$(echo "$available_ram_gb * 0.40 * 1024" | bc | awk '{print int($1)}')
            ;;
        aggressive)
            # Use 60% of available RAM
            local memory=$(echo "$available_ram_gb * 0.60 * 1024" | bc | awk '{print int($1)}')
            ;;
        *)
            local memory=2048
            ;;
    esac

    # Minimum 1GB, maximum 8GB for local dev
    if [ "$memory" -lt 1024 ]; then
        memory=1024
    elif [ "$memory" -gt 8192 ]; then
        memory=8192
    fi

    echo "$memory"
}

# Determine if full parallelization is safe
can_use_full_parallel() {
    local available_cores=$1
    local available_ram_gb=$2
    local min_cores=${3:-4}
    local min_ram_gb=${4:-4}

    if [ "$available_cores" -ge "$min_cores" ] && \
       [ "$(echo "$available_ram_gb >= $min_ram_gb" | bc)" -eq 1 ]; then
        echo "true"
    else
        echo "false"
    fi
}

# Generate resource report
generate_report() {
    local mode=${1:-"balanced"}
    local format=${2:-"text"}

    log_info "Detecting system resources..."

    local os=$(detect_os)
    local total_cores=$(get_cpu_cores)
    local available_cores=$(get_available_cpu_cores)
    local total_ram=$(get_total_ram_gb)
    local available_ram=$(get_available_ram_gb)
    local playwright_workers=$(calculate_playwright_workers "$available_cores" "$available_ram" "$mode")
    local node_memory=$(calculate_node_memory "$available_ram" "$mode")
    local can_parallel=$(can_use_full_parallel "$available_cores" "$available_ram" 4 4)

    if [ "$format" = "json" ]; then
        cat << EOF
{
  "os": "$os",
  "cpu": {
    "total_cores": $total_cores,
    "available_cores": $available_cores
  },
  "memory": {
    "total_gb": $total_ram,
    "available_gb": $available_ram
  },
  "recommendations": {
    "mode": "$mode",
    "playwright_workers": $playwright_workers,
    "node_memory_mb": $node_memory,
    "can_use_full_parallel": $can_parallel
  }
}
EOF
    else
        cat << EOF

${BLUE}════════════════════════════════════════════════════════════════${NC}
${GREEN}                    Resource Detection Report                    ${NC}
${BLUE}════════════════════════════════════════════════════════════════${NC}

${YELLOW}System Information:${NC}
  Operating System:     $os

${YELLOW}CPU Resources:${NC}
  Total Cores:          $total_cores
  Available Cores:      $available_cores

${YELLOW}Memory Resources:${NC}
  Total RAM:            ${total_ram} GB
  Available RAM:        ${available_ram} GB

${BLUE}────────────────────────────────────────────────────────────────${NC}

${YELLOW}Optimization Mode:${NC} $mode

${YELLOW}Recommended Settings:${NC}
  Playwright Workers:   $playwright_workers
  Node Memory Limit:    ${node_memory} MB
  Full Parallelization: $([ "$can_parallel" = "true" ] && echo "${GREEN}✅ SAFE${NC}" || echo "${RED}❌ NOT RECOMMENDED${NC}")

${BLUE}────────────────────────────────────────────────────────────────${NC}

${YELLOW}Export Commands:${NC}
  export PLAYWRIGHT_WORKERS=$playwright_workers
  export NODE_OPTIONS=--max-old-space-size=$node_memory
  export FULL_PARALLEL=$can_parallel

${YELLOW}Usage Examples:${NC}
  # Run tests with detected settings
  make test-auto

  # Override with aggressive mode
  bash scripts/detect_resources.sh --mode=aggressive --apply

  # Generate JSON for CI/CD
  bash scripts/detect_resources.sh --format=json > resources.json

${BLUE}════════════════════════════════════════════════════════════════${NC}

EOF
    fi
}

# Apply detected settings to environment
apply_settings() {
    local mode=${1:-"balanced"}

    local available_cores=$(get_available_cpu_cores)
    local available_ram=$(get_available_ram_gb)
    local playwright_workers=$(calculate_playwright_workers "$available_cores" "$available_ram" "$mode")
    local node_memory=$(calculate_node_memory "$available_ram" "$mode")
    local can_parallel=$(can_use_full_parallel "$available_cores" "$available_ram" 4 4)

    # Export to environment
    export PLAYWRIGHT_WORKERS=$playwright_workers
    export NODE_OPTIONS="--max-old-space-size=$node_memory"
    export FULL_PARALLEL=$can_parallel
    export RESOURCE_MODE=$mode

    log_success "Settings applied to environment"
    log_info "PLAYWRIGHT_WORKERS=$playwright_workers"
    log_info "NODE_OPTIONS=$NODE_OPTIONS"
    log_info "FULL_PARALLEL=$can_parallel"
}

# Update Playwright config dynamically
update_playwright_config() {
    local mode=${1:-"balanced"}
    local config_file=${2:-"frontend/playwright.config.ts"}

    if [ ! -f "$config_file" ]; then
        log_warning "Playwright config not found: $config_file"
        return 1
    fi

    local available_cores=$(get_available_cpu_cores)
    local available_ram=$(get_available_ram_gb)
    local workers=$(calculate_playwright_workers "$available_cores" "$available_ram" "$mode")
    local can_parallel=$(can_use_full_parallel "$available_cores" "$available_ram" 4 4)

    log_info "Updating Playwright config: $config_file"
    log_info "Workers: $workers, Full Parallel: $can_parallel"

    # Create backup
    cp "$config_file" "$config_file.bak"

    # Update config (this is a template - adjust based on actual config structure)
    cat > "$config_file.dynamic" << EOF
// Auto-generated by scripts/detect_resources.sh
// Mode: $mode
// Detected: $available_cores cores, ${available_ram} GB RAM

import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  fullyParallel: $can_parallel,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : $workers,
  reporter: 'html',
  use: {
    baseURL: 'http://127.0.0.1:5173',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
  webServer: {
    command: 'npm run dev',
    url: 'http://127.0.0.1:5173',
    reuseExistingServer: !process.env.CI,
    timeout: 120 * 1000,
  },
});
EOF

    log_success "Playwright config updated (backup: $config_file.bak)"
}

# Show help
show_help() {
    cat << EOF
Resource Detection and Adaptive Configuration Script

Usage: bash scripts/detect_resources.sh [OPTIONS]

OPTIONS:
  --mode=MODE           Optimization mode: conservative, balanced, aggressive
                        Default: balanced
  --format=FORMAT       Output format: text, json
                        Default: text
  --apply               Apply settings to current environment
  --update-playwright   Update Playwright config with detected settings
  --config=FILE         Playwright config file path
                        Default: frontend/playwright.config.ts
  --help                Show this help message

MODES:
  conservative          Use 50% of resources (safest)
  balanced              Use 75% of resources (recommended)
  aggressive            Use 100% of resources (maximum performance)

EXAMPLES:
  # Show resource report
  bash scripts/detect_resources.sh

  # Apply aggressive settings
  bash scripts/detect_resources.sh --mode=aggressive --apply

  # Update Playwright config
  bash scripts/detect_resources.sh --update-playwright

  # Generate JSON for CI/CD
  bash scripts/detect_resources.sh --format=json > resources.json

  # Use in scripts
  eval \$(bash scripts/detect_resources.sh --apply --mode=balanced)
  npm test

EOF
}

# Main execution
main() {
    local mode="balanced"
    local format="text"
    local apply=false
    local update_pw=false
    local config_file="frontend/playwright.config.ts"

    # Parse arguments
    for arg in "$@"; do
        case $arg in
            --mode=*)
                mode="${arg#*=}"
                ;;
            --format=*)
                format="${arg#*=}"
                ;;
            --apply)
                apply=true
                ;;
            --update-playwright)
                update_pw=true
                ;;
            --config=*)
                config_file="${arg#*=}"
                ;;
            --help|-h)
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

    # Validate mode
    case "$mode" in
        conservative|balanced|aggressive)
            ;;
        *)
            log_error "Invalid mode: $mode"
            log_info "Valid modes: conservative, balanced, aggressive"
            exit 1
            ;;
    esac

    # Generate report
    generate_report "$mode" "$format"

    # Apply settings if requested
    if [ "$apply" = true ]; then
        apply_settings "$mode"
    fi

    # Update Playwright config if requested
    if [ "$update_pw" = true ]; then
        update_playwright_config "$mode" "$config_file"
    fi
}

# Execute main function
main "$@"
