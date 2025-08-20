#!/bin/bash

# Install Git Hooks for enrich-ddf-floor-2
# Sets up pre-commit hooks, commit message template, and validation scripts

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR:${NC} $1" >&2
}

warning() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING:${NC} $1"
}

info() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')] INFO:${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    log "Checking prerequisites..."

    # Check if we're in a git repository
    if [ ! -d ".git" ]; then
        error "Not in a git repository. Please run this script from the project root."
        exit 1
    fi

    # Check if required directories exist
    if [ ! -d "scripts/hooks" ]; then
        error "scripts/hooks directory not found. Please ensure you're in the correct project directory."
        exit 1
    fi

    # Check if validation scripts exist
    if [ ! -f "scripts/hooks/validate-taxonomy.sh" ]; then
        error "Taxonomy validation script not found at scripts/hooks/validate-taxonomy.sh"
        exit 1
    fi

    if [ ! -f "scripts/hooks/protect-api-keys.sh" ]; then
        error "API key protection script not found at scripts/hooks/protect-api-keys.sh"
        exit 1
    fi

    log "✅ Prerequisites check passed"
}

# Make scripts executable
make_scripts_executable() {
    log "Making hook scripts executable..."

    chmod +x scripts/hooks/validate-taxonomy.sh
    chmod +x scripts/hooks/protect-api-keys.sh

    log "✅ Hook scripts are now executable"
}

# Install pre-commit using pip (if not already installed)
install_pre_commit() {
    log "Checking for pre-commit installation..."

    if command -v pre-commit >/dev/null 2>&1; then
        log "✅ pre-commit is already installed"
        pre-commit --version
    else
        warning "pre-commit not found. Installing via pip..."
        
        # Try to install pre-commit
        if command -v pip >/dev/null 2>&1; then
            pip install pre-commit
            log "✅ pre-commit installed successfully"
        elif command -v pip3 >/dev/null 2>&1; then
            pip3 install pre-commit
            log "✅ pre-commit installed successfully"
        else
            error "pip not found. Please install pre-commit manually:"
            error "  pip install pre-commit"
            error "  or visit: https://pre-commit.com/#install"
            exit 1
        fi
    fi
}

# Install pre-commit hooks
install_pre_commit_hooks() {
    log "Installing pre-commit hooks..."

    # Install the hooks defined in .pre-commit-config.yaml
    if pre-commit install; then
        log "✅ Pre-commit hooks installed successfully"
    else
        error "Failed to install pre-commit hooks"
        exit 1
    fi

    # Also install pre-push hooks
    if pre-commit install --hook-type pre-push; then
        log "✅ Pre-push hooks installed successfully"
    else
        warning "Failed to install pre-push hooks (this is optional)"
    fi
}

# Set up commit message template
setup_commit_template() {
    log "Setting up commit message template..."

    if [ -f ".gitmessage" ]; then
        # Configure git to use the commit template
        git config commit.template .gitmessage
        log "✅ Commit message template configured"
        
        info "You can now use 'git commit' (without -m) to open the template"
    else
        warning "Commit message template (.gitmessage) not found"
    fi
}

# Test the installation
test_installation() {
    log "Testing git hooks installation..."

    # Test taxonomy validation
    info "Testing taxonomy validation..."
    if scripts/hooks/validate-taxonomy.sh; then
        log "✅ Taxonomy validation test passed"
    else
        warning "⚠️  Taxonomy validation found issues (this may be expected)"
        warning "    Run 'scripts/hooks/validate-taxonomy.sh' to see details"
    fi

    # Test API key protection
    info "Testing API key protection..."
    if scripts/hooks/protect-api-keys.sh; then
        log "✅ API key protection test passed"
    else
        warning "⚠️  API key protection found issues"
        warning "    Run 'scripts/hooks/protect-api-keys.sh' to see details"
    fi

    # Test pre-commit
    info "Testing pre-commit installation..."
    if pre-commit run --all-files --show-diff-on-failure; then
        log "✅ Pre-commit hooks test passed"
    else
        warning "⚠️  Pre-commit hooks found issues"
        warning "    This is normal for initial setup - fix issues and commit"
    fi
}

# Create .gitignore entries for hook-related files
update_gitignore() {
    log "Updating .gitignore for hook-related files..."

    local gitignore_entries=(
        "# Git hooks and pre-commit"
        ".pre-commit-config.yaml.backup"
        "*.orig"
        "*.rej"
    )

    local needs_update=false
    for entry in "${gitignore_entries[@]}"; do
        if ! grep -Fxq "$entry" .gitignore 2>/dev/null; then
            echo "$entry" >> .gitignore
            needs_update=true
        fi
    done

    if [ "$needs_update" = true ]; then
        log "✅ Updated .gitignore with hook-related entries"
    else
        log "✅ .gitignore already contains hook-related entries"
    fi
}

# Display usage information
show_usage() {
    log "Git hooks installation completed! 🎉"
    echo ""
    echo -e "${BLUE}📋 What was installed:${NC}"
    echo "  ✅ Pre-commit hooks (.pre-commit-config.yaml)"
    echo "  ✅ Taxonomy validation (scripts/hooks/validate-taxonomy.sh)"
    echo "  ✅ API key protection (scripts/hooks/protect-api-keys.sh)"
    echo "  ✅ Commit message template (.gitmessage)"
    echo ""
    echo -e "${BLUE}🚀 How to use:${NC}"
    echo "  • Hooks run automatically on 'git commit' and 'git push'"
    echo "  • Use 'git commit' (no -m) to open commit template"
    echo "  • Manual validation: 'scripts/hooks/validate-taxonomy.sh'"
    echo "  • Manual API check: 'scripts/hooks/protect-api-keys.sh'"
    echo "  • Skip hooks (emergency): 'git commit --no-verify'"
    echo ""
    echo -e "${BLUE}🔧 Configuration:${NC}"
    echo "  • Edit .pre-commit-config.yaml to modify hook behavior"
    echo "  • Edit .gitmessage to customize commit template"
    echo "  • Hooks validate: code quality, API keys, project structure"
    echo ""
    echo -e "${YELLOW}⚠️  Important:${NC}"
    echo "  • Hooks will prevent commits with real API keys"
    echo "  • Use placeholder values in committed files"
    echo "  • Keep real API keys in local .env file only"
    echo ""
}

# Main installation function
main() {
    echo -e "${GREEN}🔧 Installing Git Hooks for enrich-ddf-floor-2${NC}"
    echo "=================================================="
    echo ""

    check_prerequisites
    make_scripts_executable
    install_pre_commit
    install_pre_commit_hooks
    setup_commit_template
    update_gitignore
    
    echo ""
    echo -e "${GREEN}🧪 Testing installation...${NC}"
    test_installation
    
    echo ""
    show_usage
}

# Handle help option
if [ "${1:-}" = "--help" ] || [ "${1:-}" = "-h" ]; then
    echo "Git Hooks Installation Script for enrich-ddf-floor-2"
    echo ""
    echo "Usage: $0 [options]"
    echo ""
    echo "Options:"
    echo "  -h, --help    Show this help message"
    echo ""
    echo "This script installs:"
    echo "  • Pre-commit hooks for code quality and security"
    echo "  • Taxonomy validation for project structure"
    echo "  • API key protection to prevent credential leaks"
    echo "  • Structured commit message template"
    echo ""
    exit 0
fi

# Run main function
main "$@"
