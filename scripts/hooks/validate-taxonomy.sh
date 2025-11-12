#!/bin/bash

# Taxonomy Validation Script for enrich-ddf-floor-2
# Validates project directory structure and file placement

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${GREEN}[TAXONOMY]${NC} $1"
}

error() {
    echo -e "${RED}[TAXONOMY ERROR]${NC} $1" >&2
}

warning() {
    echo -e "${YELLOW}[TAXONOMY WARNING]${NC} $1"
}

# Validate core directory structure
validate_core_structure() {
    local errors=0

    log "Checking core directory structure..."

    # Required directories
    local required_dirs=("core" "data" "services" "tests" "frontend" "database")
    for dir in "${required_dirs[@]}"; do
        if [ ! -d "$dir" ]; then
            error "Required directory missing: $dir"
            errors=$((errors + 1))
        else
            log "✅ Required directory exists: $dir"
        fi
    done

    # Check for proper subdirectory structure
    if [ -d "core" ]; then
        local core_subdirs=("enrichment" "integrations" "utils")
        for subdir in "${core_subdirs[@]}"; do
            if [ ! -d "core/$subdir" ]; then
                warning "Core subdirectory missing: core/$subdir"
            fi
        done
    fi

    if [ -d "services" ]; then
        local service_subdirs=("third_party" "government_apis" "web_crawlers")
        for subdir in "${service_subdirs[@]}"; do
            if [ ! -d "services/$subdir" ]; then
                warning "Services subdirectory missing: services/$subdir"
            fi
        done
    fi

    return $errors
}

# Validate file placement rules
validate_file_placement() {
    local errors=0

    log "Checking file placement rules..."

    # Check for Python files in wrong locations
    local misplaced_python=0
    while IFS= read -r file; do
        # Skip acceptable locations
        if [[ "$file" == "./venv/"* ]] || \
           [[ "$file" == "./node_modules/"* ]] || \
           [[ "$file" == "./frontend/node_modules/"* ]] || \
           [[ "$file" == "./__pycache__/"* ]] || \
           [[ "$file" == "./tests/"* ]] || \
           [[ "$file" == "./core/"* ]] || \
           [[ "$file" == "./services/"* ]] || \
           [[ "$file" == "./database/"* ]] || \
           [[ "$file" == "./data/"* ]] || \
           [[ "$file" == "./alembic/"* ]] || \
           [[ "$file" == "./scripts/"* ]] || \
           [[ "$file" == "./main.py" ]] || \
           [[ "$file" == "./config.py" ]]; then
            continue
        fi

        error "Python file in wrong location: $file"
        error "  → Move to appropriate subdirectory (core/, services/, database/, etc.)"
        misplaced_python=1
    done < <(find . -name "*.py" -type f \
        -not -path "./venv/*" \
        -not -path "./node_modules/*" \
        -not -path "./frontend/node_modules/*" \
        -not -path "./__pycache__/*" \
        2>/dev/null)

    if [ $misplaced_python -eq 1 ]; then
        errors=$((errors + 1))
    fi

    # Check for test files outside tests/ directory
    local misplaced_tests=0
    while IFS= read -r file; do
        # Skip files already in tests/ directory
        if [[ "$file" == "./tests/"* ]]; then
            continue
        fi

        # Skip frontend test files (they belong in frontend/tests/)
        if [[ "$file" == "./frontend/tests/"* ]]; then
            continue
        fi

        # Skip node_modules, venv, and other acceptable locations
        if [[ "$file" == "./venv/"* ]] || \
           [[ "$file" == "./node_modules/"* ]] || \
           [[ "$file" == "./frontend/node_modules/"* ]] || \
           [[ "$file" == "./.cursor/"* ]] || \
           [[ "$file" == "./scripts/test_"* ]]; then
            continue
        fi

        error "Test file should be in tests/ directory: $file"
        misplaced_tests=1
    done < <(find . -name "*test*.py" -o -name "*test*.js" -o -name "*test*.ts" -o -name "test_*" \
        | grep -v "./tests/" \
        | grep -v "./frontend/tests/" \
        | grep -v "./venv/" \
        | grep -v "./node_modules/" \
        | grep -v "./frontend/node_modules/" \
        | grep -v "./.cursor/" \
        2>/dev/null)

    if [ $misplaced_tests -eq 1 ]; then
        errors=$((errors + 1))
    fi

    return $errors
}

# Validate configuration management
validate_configuration() {
    local errors=0

    log "Checking configuration management..."

    # Check for .env file structure
    if [ -f ".env" ]; then
        log "✅ Environment file exists"

        # Check for real API keys (basic patterns)
        local real_keys=0
        if grep -q "AKIA[0-9A-Z]\{16\}" .env 2>/dev/null; then
            error "Real AWS access key detected in .env file"
            real_keys=1
        fi

        if grep -q "sk-[a-zA-Z0-9]\{48\}" .env 2>/dev/null; then
            error "Real OpenAI API key detected in .env file"
            real_keys=1
        fi

        if [ $real_keys -eq 1 ]; then
            error "Remove real API keys from .env file"
            error "Use .env.example for templates and keep real keys local"
            errors=$((errors + 1))
        fi
    else
        warning "No .env file found - create one from .env.example"
    fi

    # Check for .env.example
    if [ ! -f ".env.example" ]; then
        warning "No .env.example template found"
    else
        log "✅ Environment template exists"
    fi

    return $errors
}

# Validate documentation structure
validate_documentation() {
    local errors=0

    log "Checking documentation structure..."

    # Check for essential documentation
    local required_docs=("README.md" "QUICK_REFERENCE.md")
    for doc in "${required_docs[@]}"; do
        if [ ! -f "$doc" ]; then
            warning "Missing documentation: $doc"
        else
            log "✅ Documentation exists: $doc"
        fi
    done

    # Check for active plans directory
    if [ -d "active" ]; then
        log "✅ Active plans directory exists"

        # Check if there are active plans
        local plan_count=$(find active/ -name "*.md" 2>/dev/null | wc -l)
        if [ "$plan_count" -eq 0 ]; then
            warning "No active plans found in active/ directory"
        else
            log "✅ Found $plan_count active plan(s)"
        fi
    else
        warning "No active/ directory found for project plans"
    fi

    return $errors
}

# Validate temporary and cache directories
validate_temporary_structure() {
    local errors=0

    log "Checking temporary file management..."

    # Check for temporary files in project root
    local temp_files_at_root=0
    local temp_patterns=("*.tmp" "*.temp" "temp_*" "tmp_*")
    for pattern in "${temp_patterns[@]}"; do
        if ls $pattern 2>/dev/null | head -1 >/dev/null; then
            error "Temporary files found in project root: $pattern"
            error "  → Move to .tmp/ directory for automatic cleanup"
            temp_files_at_root=1
        fi
    done

    if [ $temp_files_at_root -eq 1 ]; then
        errors=$((errors + 1))
    fi

    # Check for cache directories in wrong locations
    local cache_dirs=("__pycache__" ".pytest_cache" ".mypy_cache" "node_modules")
    for cache_dir in "${cache_dirs[@]}"; do
        if [ -d "$cache_dir" ] && [[ "$cache_dir" != "./"* ]]; then
            log "✅ Cache directory properly located: $cache_dir"
        fi
    done

    return $errors
}

# Validate frontend structure (if exists)
validate_frontend_structure() {
    local errors=0

    if [ ! -d "frontend" ]; then
        log "No frontend directory - skipping frontend validation"
        return 0
    fi

    log "Checking frontend structure..."

    # Check for essential frontend files
    local frontend_files=("package.json" "tsconfig.json" "vite.config.ts")
    for file in "${frontend_files[@]}"; do
        if [ ! -f "frontend/$file" ]; then
            warning "Missing frontend file: frontend/$file"
        else
            log "✅ Frontend file exists: frontend/$file"
        fi
    done

    # Check for proper src structure
    if [ -d "frontend/src" ]; then
        local src_dirs=("components" "pages" "services" "types" "hooks")
        for dir in "${src_dirs[@]}"; do
            if [ ! -d "frontend/src/$dir" ]; then
                warning "Frontend src subdirectory missing: frontend/src/$dir"
            else
                log "✅ Frontend src directory exists: frontend/src/$dir"
            fi
        done
    else
        error "Frontend src directory missing: frontend/src"
        errors=$((errors + 1))
    fi

    return $errors
}

# Validate database structure
validate_database_structure() {
    local errors=0

    log "Checking database structure..."

    if [ -d "database" ]; then
        # Check for database modules
        local db_modules=("models" "utils" "migrations")
        for module in "${db_modules[@]}"; do
            if [ ! -d "database/$module" ]; then
                warning "Database module missing: database/$module"
            else
                log "✅ Database module exists: database/$module"
            fi
        done

        # Check for essential database files
        if [ ! -f "database/__init__.py" ]; then
            error "Database __init__.py missing"
            errors=$((errors + 1))
        fi

        if [ ! -f "database/connection.py" ]; then
            error "Database connection.py missing"
            errors=$((errors + 1))
        fi
    else
        error "Database directory missing"
        errors=$((errors + 1))
    fi

    return $errors
}

# Main validation function
main() {
    local total_errors=0
    local total_warnings=0

    log "Starting taxonomy validation for enrich-ddf-floor-2..."

    # Run validation checks
    validate_core_structure
    total_errors=$((total_errors + $?))

    validate_file_placement
    total_errors=$((total_errors + $?))

    validate_configuration
    total_errors=$((total_errors + $?))

    validate_documentation
    total_errors=$((total_errors + $?))

    validate_temporary_structure
    total_errors=$((total_errors + $?))

    validate_frontend_structure
    total_errors=$((total_errors + $?))

    validate_database_structure
    total_errors=$((total_errors + $?))

    # Report results
    if [ $total_errors -eq 0 ]; then
        echo "✅ [SUCCESS] 🎉 All taxonomy validation checks passed!"
        log "✅ Project structure is well-organized"
        return 0
    else
        echo "❌ [ERROR] Taxonomy validation failed with $total_errors errors"
        error "❌ Fix project structure issues before committing"
        echo ""
        error "Common fixes:"
        error "1. Move Python files to appropriate directories (core/, services/, database/)"
        error "2. Move test files to tests/ directory"
        error "3. Remove real API keys from .env file"
        error "4. Move temporary files to .tmp/ directory"
        error "5. Ensure required directories exist"
        echo ""
        return 1
    fi
}

# Run validation
main "$@"
