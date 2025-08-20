#!/bin/bash

# Fast API Key Protection Script for enrich-ddf-floor-2
# Quick checks to prevent committing real API keys and sensitive credentials

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${GREEN}[API-PROTECTION]${NC} $1"
}

error() {
    echo -e "${RED}[API-PROTECTION ERROR]${NC} $1" >&2
}

warning() {
    echo -e "${YELLOW}[API-PROTECTION WARNING]${NC} $1"
}

# Quick check for real API keys in .env files
check_env_files_fast() {
    local errors=0

    log "Checking .env files for real credentials..."

    # Check .env file if it exists
    if [ -f ".env" ]; then
        # Check for real API key patterns
        if grep -E "(AKIA[0-9A-Z]{16}|sk-[a-zA-Z0-9]{48})" .env >/dev/null 2>&1; then
            error "Real API keys detected in .env file!"
            error "  → Replace with placeholder values like 'your_api_key_here'"
            error "  → Keep real credentials in local .env file only"
            errors=$((errors + 1))
        fi
        
        # Check for other suspicious patterns
        if grep -E "(=[a-f0-9]{40}|=xoxb-[0-9]+-)" .env >/dev/null 2>&1; then
            warning "Potential real credentials detected in .env file"
            warning "  → Verify these are not real API keys"
        fi
    fi

    # Check .env.template if it exists
    if [ -f ".env.template" ]; then
        if grep -E "(AKIA[0-9A-Z]{16}|sk-[a-zA-Z0-9]{48})" .env.template >/dev/null 2>&1; then
            error "Real API keys detected in .env.template file!"
            error "  → Template files should only contain placeholders"
            errors=$((errors + 1))
        fi
    fi

    return $errors
}

# Check for sensitive files in project root
check_sensitive_files_fast() {
    local errors=0

    log "Checking for sensitive files..."

    # Check for common sensitive file patterns in project root
    local sensitive_files=0
    
    # Private keys
    if ls *.pem *.key *_rsa id_rsa* 2>/dev/null | head -1 >/dev/null; then
        error "Private key files detected in project root!"
        ls *.pem *.key *_rsa id_rsa* 2>/dev/null | head -3
        error "  → Remove or add to .gitignore"
        sensitive_files=1
    fi
    
    # Certificates
    if ls *.crt *.cer *.p12 *.pfx 2>/dev/null | head -1 >/dev/null; then
        error "Certificate files detected in project root!"
        ls *.crt *.cer *.p12 *.pfx 2>/dev/null | head -3
        error "  → Remove or add to .gitignore"
        sensitive_files=1
    fi

    if [ $sensitive_files -eq 1 ]; then
        errors=$((errors + 1))
    fi

    return $errors
}

# Check for large database files
check_database_files_fast() {
    local errors=0

    log "Checking for large database files..."

    # Check for database files in project root
    local large_db=0
    for db_file in *.db *.sqlite *.sqlite3; do
        if [ -f "$db_file" ]; then
            local size
            size=$(stat -f%z "$db_file" 2>/dev/null || stat -c%s "$db_file" 2>/dev/null || echo 0)
            if [ "$size" -gt 1048576 ]; then  # 1MB
                error "Large database file detected: $db_file (${size} bytes)"
                error "  → Add to .gitignore or use smaller test database"
                large_db=1
            fi
        fi
    done

    if [ $large_db -eq 1 ]; then
        errors=$((errors + 1))
    fi

    return $errors
}

# Check staged files for API keys (git pre-commit context)
check_staged_files() {
    local errors=0

    # Only run if we're in a git repository and have staged files
    if command -v git >/dev/null 2>&1 && git rev-parse --git-dir >/dev/null 2>&1; then
        local staged_files
        staged_files=$(git diff --cached --name-only 2>/dev/null || true)
        
        if [ -n "$staged_files" ]; then
            log "Checking staged files for API keys..."
            
            # Check each staged file for API key patterns
            while IFS= read -r file; do
                if [ -f "$file" ] && [[ "$file" =~ \.(py|js|ts|tsx|json|yaml|yml|env)$ ]]; then
                    # Quick check for common API key patterns
                    if git show ":$file" 2>/dev/null | grep -E "(AKIA[0-9A-Z]{16}|sk-[a-zA-Z0-9]{48})" >/dev/null; then
                        error "Real API key detected in staged file: $file"
                        error "  → Remove real API keys before committing"
                        errors=$((errors + 1))
                    fi
                fi
            done <<< "$staged_files"
        fi
    fi

    return $errors
}

# Main protection function
main() {
    local total_errors=0

    log "Starting fast API key protection scan..."

    # Run fast protection checks
    check_env_files_fast
    total_errors=$((total_errors + $?))

    check_sensitive_files_fast
    total_errors=$((total_errors + $?))

    check_database_files_fast
    total_errors=$((total_errors + $?))

    check_staged_files
    total_errors=$((total_errors + $?))

    # Report results
    if [ $total_errors -eq 0 ]; then
        echo "✅ [SUCCESS] 🔒 No sensitive credentials detected!"
        log "✅ API key protection passed"
        return 0
    else
        echo "❌ [ERROR] Sensitive credentials detected - commit blocked!"
        error "❌ Fix credential issues before committing"
        echo ""
        error "Security fixes:"
        error "1. Replace real API keys with placeholders (your_api_key_here)"
        error "2. Remove sensitive files or add to .gitignore"
        error "3. Use .env.example for templates, keep real .env local"
        error "4. Never commit private keys, certificates, or tokens"
        echo ""
        return 1
    fi
}

# Run protection
main "$@"
