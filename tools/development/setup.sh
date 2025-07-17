#!/bin/bash
# Development Environment Setup Script
# Enrich DDF Floor 2 - Complete developer onboarding automation

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
ENV_FILE="${PROJECT_ROOT}/.env"
VSCODE_SETTINGS="${PROJECT_ROOT}/.vscode/settings.json"

echo -e "${BLUE}🚀 Enrich DDF Floor 2 - Development Environment Setup${NC}"
echo "============================================================"
echo "Project Root: ${PROJECT_ROOT}"
echo ""

# Change to project root
cd "${PROJECT_ROOT}"

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to log setup steps
log_step() {
    echo -e "${CYAN}📋 $1${NC}"
}

# Function to log success
log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

# Function to log warning
log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Function to log error
log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# 1. Check system requirements
log_step "Checking system requirements..."

# Check Python version
if command_exists python3; then
    PYTHON_VERSION=$(python3 --version | cut -d " " -f 2)
    log_success "Python found: $PYTHON_VERSION"
    
    # Check if Python 3.11+
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
    
    if [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -ge 11 ]; then
        log_success "Python version is compatible (3.11+)"
    else
        log_warning "Python 3.11+ recommended, found $PYTHON_VERSION"
    fi
else
    log_error "Python3 not found. Please install Python 3.11+"
    exit 1
fi

# Check Git
if command_exists git; then
    GIT_VERSION=$(git --version | cut -d " " -f 3)
    log_success "Git found: $GIT_VERSION"
else
    log_error "Git not found. Please install Git"
    exit 1
fi

# Check Docker
if command_exists docker; then
    DOCKER_VERSION=$(docker --version | cut -d " " -f 3 | sed 's/,//')
    log_success "Docker found: $DOCKER_VERSION"
else
    log_warning "Docker not found. Install Docker for containerized development"
fi

# Check Docker Compose
if command_exists docker-compose; then
    COMPOSE_VERSION=$(docker-compose --version | cut -d " " -f 3 | sed 's/,//')
    log_success "Docker Compose found: $COMPOSE_VERSION"
else
    log_warning "Docker Compose not found. Install for multi-service development"
fi

# 2. Check and install Poetry
log_step "Setting up Python dependency management..."

if command_exists poetry; then
    POETRY_VERSION=$(poetry --version | cut -d " " -f 3)
    log_success "Poetry found: $POETRY_VERSION"
else
    log_step "Installing Poetry..."
    curl -sSL https://install.python-poetry.org | python3 -
    
    # Add Poetry to PATH for current session
    export PATH="$HOME/.local/bin:$PATH"
    
    if command_exists poetry; then
        log_success "Poetry installed successfully"
    else
        log_error "Poetry installation failed. Please install manually"
        exit 1
    fi
fi

# Configure Poetry
log_step "Configuring Poetry..."
poetry config virtualenvs.in-project true
poetry config virtualenvs.prefer-active-python true
log_success "Poetry configured for in-project virtual environments"

# 3. Install project dependencies
log_step "Installing project dependencies..."

if [ -f "pyproject.toml" ]; then
    echo "Installing production dependencies..."
    poetry install
    
    echo "Installing development dependencies..."
    poetry install --with dev
    
    log_success "All dependencies installed"
else
    log_error "pyproject.toml not found. Cannot install dependencies"
    exit 1
fi

# 4. Set up environment configuration
log_step "Setting up environment configuration..."

if [ ! -f "$ENV_FILE" ]; then
    log_step "Creating .env file from template..."
    
    if [ -f "env.example" ]; then
        cp env.example .env
        log_success ".env file created from template"
    else
        # Create basic .env file
        cat > .env << EOF
# Enrich DDF Floor 2 - Development Environment Configuration

# Application Settings
DEBUG=true
SECRET_KEY=dev-secret-key-change-in-production-$(openssl rand -hex 16)
ENVIRONMENT=development

# Database Configuration
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5433/enrich_ddf_floor2

# Redis Configuration  
REDIS_URL=redis://localhost:6379/0

# Celery Configuration
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/2

# External API Keys (Add your keys here)
# APOLLO_API_KEY=your_apollo_api_key_here
# PEOPLEDATALABS_API_KEY=your_peopledatalabs_api_key_here
# ZEROBOUNCE_API_KEY=your_zerobounce_api_key_here

# Logging Configuration
LOG_LEVEL=DEBUG
LOG_FORMAT=json

# Development Settings
DEV_MODE=true
HOT_RELOAD=true
EOF
        log_success "Basic .env file created"
    fi
else
    log_success ".env file already exists"
fi

# 5. Set up pre-commit hooks
log_step "Setting up pre-commit hooks..."

if poetry run pre-commit --version >/dev/null 2>&1; then
    poetry run pre-commit install
    log_success "Pre-commit hooks installed"
else
    log_warning "Pre-commit not available. Install development dependencies first"
fi

# 6. Set up VS Code configuration
log_step "Setting up IDE configuration..."

if [ -f "$VSCODE_SETTINGS" ]; then
    log_success "VS Code settings already configured"
else
    log_warning "VS Code settings not found. Manual IDE setup may be required"
fi

# 7. Initialize database (if Docker is available)
if command_exists docker && command_exists docker-compose; then
    log_step "Setting up development database..."
    
    if [ -f "docker-compose.yml" ]; then
        echo "Starting development database..."
        docker-compose up -d db redis
        
        # Wait for database to be ready
        echo "Waiting for database to be ready..."
        sleep 10
        
        log_success "Development database started"
    else
        log_warning "docker-compose.yml not found. Database setup skipped"
    fi
else
    log_warning "Docker not available. Database setup skipped"
fi

# 8. Run initial tests
log_step "Running initial project validation..."

# Check if basic imports work
if poetry run python -c "import app" 2>/dev/null; then
    log_success "Application imports successfully"
else
    log_warning "Application import failed. Check dependencies"
fi

# Run linting if available
if [ -f "tools/linting/lint.sh" ]; then
    echo "Running code quality checks..."
    if ./tools/linting/lint.sh; then
        log_success "All quality checks passed"
    else
        log_warning "Some quality checks failed. Run ./tools/linting/format.sh to fix"
    fi
fi

# 9. Display setup summary
echo ""
echo -e "${BLUE}📊 Setup Summary${NC}"
echo "========================================"
echo -e "Project: ${GREEN}Enrich DDF Floor 2${NC}"
echo -e "Environment: ${GREEN}Development${NC}"
echo -e "Python: ${GREEN}$(python3 --version)${NC}"

if command_exists poetry; then
    echo -e "Poetry: ${GREEN}$(poetry --version)${NC}"
fi

if [ -f ".venv/pyvenv.cfg" ]; then
    echo -e "Virtual Environment: ${GREEN}✅ Created${NC}"
fi

if [ -f "$ENV_FILE" ]; then
    echo -e "Environment Config: ${GREEN}✅ Configured${NC}"
fi

echo ""
echo -e "${BLUE}🎯 Next Steps${NC}"
echo "========================================"
echo "1. Review and update .env file with your API keys"
echo "2. Start development server: poetry run uvicorn app.main:app --reload"
echo "3. Run tests: poetry run pytest"
echo "4. Check code quality: ./tools/linting/lint.sh"
echo "5. Format code: ./tools/linting/format.sh"
echo ""
echo -e "${GREEN}🎉 Development environment setup complete!${NC}"
echo "Happy coding! 🚀" 