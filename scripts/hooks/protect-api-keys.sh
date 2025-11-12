#!/bin/bash

# API Key Protection Script for enrich-ddf-floor-2
# Prevents committing real API keys and sensitive credentials

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

# Check for real API keys in files
check_api_keys() {
    local errors=0

    log "Scanning for real API keys..."

    # Define patterns for real API keys
    local patterns=(
        "AKIA[0-9A-Z]{16}"                    # AWS Access Key
        "sk-[a-zA-Z0-9]{48}"                  # OpenAI API Key
        "xoxb-[0-9]+-[0-9]+-[0-9]+-[a-z0-9]+" # Slack Bot Token
        "ghp_[a-zA-Z0-9]{36}"                 # GitHub Personal Access Token
        "gho_[a-zA-Z0-9]{36}"                 # GitHub OAuth Token
        "ghu_[a-zA-Z0-9]{36}"                 # GitHub User Token
        "ghs_[a-zA-Z0-9]{36}"                 # GitHub Server Token
        "ghr_[a-zA-Z0-9]{36}"                 # GitHub Refresh Token
        "AIza[0-9A-Za-z\\-_]{35}"             # Google API Key
        "[0-9a-f]{32}"                        # Generic 32-char hex (potential API key)
    )

    # Files to check (exclude certain directories and file types)
    local files_to_check
    files_to_check=$(find . -type f \
        \( -name "*.py" -o \
           -name "*.js" -o \
           -name "*.ts" -o \
           -name "*.tsx" -o \
           -name "*.json" -o \
           -name "*.yaml" -o \
           -name "*.yml" -o \
           -name "*.env*" -o \
           -name "*.conf" -o \
           -name "*.config" \) \
        -not -path "./venv/*" \
        -not -path "./node_modules/*" \
        -not -path "./frontend/node_modules/*" \
        -not -path "./__pycache__/*" \
        -not -path "./.git/*" \
        -not -path "./htmlcov/*" \
        -not -path "./.tmp/*" \
        -not -path "./frontend/dist/*" \
        -not -path "./dist/*" \
        2>/dev/null || true)

    # Check each pattern against each file
    for pattern in "${patterns[@]}"; do
        local found_keys=0

        while IFS= read -r file; do
            if [ -f "$file" ]; then
                # Use grep with extended regex to find patterns
                local matches
                matches=$(grep -E "$pattern" "$file" 2>/dev/null || true)

                if [ -n "$matches" ]; then
                    # Additional validation to reduce false positives
                    case "$pattern" in
                        "AKIA[0-9A-Z]{16}")
                            # AWS keys should not be in template placeholders
                            if echo "$matches" | grep -v "your_.*_key_here" | grep -v "AKIA.*EXAMPLE" | head -1 >/dev/null; then
                                error "Real AWS Access Key detected in: $file"
                                error "  Pattern: AKIA... (AWS Access Key)"
                                found_keys=1
                            fi
                            ;;
                        "sk-[a-zA-Z0-9]{48}")
                            # OpenAI keys should not be in template placeholders
                            if echo "$matches" | grep -v "your_.*_key_here" | grep -v "sk-.*EXAMPLE" | head -1 >/dev/null; then
                                error "Real OpenAI API Key detected in: $file"
                                error "  Pattern: sk-... (OpenAI API Key)"
                                found_keys=1
                            fi
                            ;;
                        *)
                            # For other patterns, check if they're not obviously placeholders
                            if echo "$matches" | grep -v "your_.*_key_here" | grep -v "EXAMPLE" | grep -v "placeholder" | head -1 >/dev/null; then
                                warning "Potential API key detected in: $file"
                                warning "  Pattern: $pattern"
                                warning "  Please verify this is not a real credential"
                            fi
                            ;;
                    esac
                fi
            fi
        done <<< "$files_to_check"

        if [ $found_keys -eq 1 ]; then
            errors=$((errors + 1))
        fi
    done

    return $errors
}

# Check for sensitive files that shouldn't be committed
check_sensitive_files() {
    local errors=0

    log "Checking for sensitive files..."

    # Patterns for sensitive files
    local sensitive_patterns=(
        "*.pem"
        "*.key"
        "*.p12"
        "*.pfx"
        "*_rsa"
        "*_dsa"
        "*_ecdsa"
        "*_ed25519"
        "*.crt"
        "*.cer"
        "id_rsa*"
        "id_dsa*"
        "id_ecdsa*"
        "id_ed25519*"
    )

    local found_sensitive=0
    for pattern in "${sensitive_patterns[@]}"; do
        local files
        files=$(find . -name "$pattern" -type f \
            -not -path "./venv/*" \
            -not -path "./node_modules/*" \
            -not -path "./frontend/node_modules/*" \
            -not -path "./.git/*" \
            -not -path "./.tmp/*" \
            2>/dev/null || true)

        if [ -n "$files" ]; then
            error "Sensitive file detected: $files"
            error "  → Remove or add to .gitignore"
            found_sensitive=1
        fi
    done

    if [ $found_sensitive -eq 1 ]; then
        errors=$((errors + 1))
    fi

    return $errors
}

# Check environment files for real credentials
check_env_files() {
    local errors=0

    log "Checking environment files..."

    # Find all .env files
    local env_files
    env_files=$(find . -name ".env*" -type f \
        -not -path "./venv/*" \
        -not -path "./node_modules/*" \
        -not -path "./frontend/node_modules/*" \
        -not -path "./.git/*" \
        2>/dev/null || true)

    local found_real_creds=0
    while IFS= read -r env_file; do
        if [ -f "$env_file" ] && [ -n "$env_file" ]; then
            # Check for patterns that indicate real credentials
            local real_cred_patterns=(
                "=AKIA[0-9A-Z]{16}"           # Real AWS key
                "=sk-[a-zA-Z0-9]{48}"         # Real OpenAI key
                "=[a-f0-9]{40}"               # 40-char hex (GitHub token)
                "=xoxb-[0-9]+-[0-9]+"         # Slack token
            )

            for pattern in "${real_cred_patterns[@]}"; do
                if grep -E "$pattern" "$env_file" >/dev/null 2>&1; then
                    error "Real credentials detected in: $env_file"
                    error "  → Use placeholder values like 'your_api_key_here'"
                    error "  → Keep real credentials in local .env file (not committed)"
                    found_real_creds=1
                    break
                fi
            done
        fi
    done <<< "$env_files"

    if [ $found_real_creds -eq 1 ]; then
        errors=$((errors + 1))
    fi

    return $errors
}

# Check for database files that shouldn't be committed
check_database_files() {
    local errors=0

    log "Checking for database files..."

    # Database file patterns
    local db_patterns=(
        "*.db"
        "*.sqlite"
        "*.sqlite3"
    )

    local found_db=0
    for pattern in "${db_patterns[@]}"; do
        local files
        files=$(find . -name "$pattern" -type f \
            -not -path "./venv/*" \
            -not -path "./node_modules/*" \
            -not -path "./frontend/node_modules/*" \
            -not -path "./.git/*" \
            -not -path "./.tmp/*" \
            2>/dev/null || true)

        if [ -n "$files" ]; then
            # Check if it's a large database file (>1MB)
            while IFS= read -r db_file; do
                if [ -f "$db_file" ]; then
                    local size
                    size=$(stat -f%z "$db_file" 2>/dev/null || stat -c%s "$db_file" 2>/dev/null || echo 0)
                    if [ "$size" -gt 1048576 ]; then  # 1MB
                        error "Large database file detected: $db_file (${size} bytes)"
                        error "  → Add to .gitignore or use smaller test database"
                        found_db=1
                    else
                        warning "Small database file found: $db_file"
                        warning "  → Consider if this should be committed"
                    fi
                fi
            done <<< "$files"
        fi
    done

    if [ $found_db -eq 1 ]; then
        errors=$((errors + 1))
    fi

    return $errors
}

# Main protection function
main() {
    local total_errors=0

    log "Starting API key and credential protection scan..."

    # Run protection checks
    check_api_keys
    total_errors=$((total_errors + $?))

    check_sensitive_files
    total_errors=$((total_errors + $?))

    check_env_files
    total_errors=$((total_errors + $?))

    check_database_files
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
        error "For real API keys, keep them in your local .env file only!"
        return 1
    fi
}

# Run protection
main "$@"
