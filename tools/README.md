# Development Tools - Enrich DDF Floor 2

This directory contains professional development tools for the Enrich DDF Floor 2 platform. All tools follow enterprise standards and provide comprehensive automation for development workflows.

## 📁 Tool Categories

### 🔧 Development Tools (`development/`)

**Purpose**: Developer productivity and environment management.

#### `setup.sh` - Development Environment Setup
Comprehensive onboarding automation for new developers.

```bash
# Full environment setup
./tools/development/setup.sh

# What it does:
# - Checks system requirements (Python 3.11+, Git, Docker)
# - Installs and configures Poetry
# - Sets up virtual environment
# - Installs all dependencies
# - Creates .env configuration
# - Sets up pre-commit hooks
# - Initializes development database
# - Runs validation checks
```

#### `dev-server.sh` - Development Server Management
Complete server lifecycle management with health monitoring.

```bash
# Start development server
./tools/development/dev-server.sh start

# Available commands:
./tools/development/dev-server.sh {start|stop|restart|status|logs|health}

# Features:
# - Automatic dependency checking
# - Database service management
# - Process monitoring with PID tracking
# - Health checks and status reporting
# - Log file management
# - Graceful shutdown handling
```

### 🗄️ Database Tools (`database/`)

**Purpose**: Database monitoring, health checks, and management.

#### `health-check.sh` - Database Health Monitoring
Comprehensive database and Redis health verification.

```bash
# Run complete health check
./tools/database/health-check.sh

# Monitors:
# - PostgreSQL connection and performance
# - Redis connectivity and statistics
# - Docker service status
# - Application database integration
# - Performance metrics
# - Configuration validation
```

### 🧪 Testing Tools (`testing/`)

**Purpose**: Automated testing suite with comprehensive coverage.

#### `test-runner.sh` - Comprehensive Test Automation
Enterprise-grade test execution with multiple test types.

```bash
# Run all tests
./tools/testing/test-runner.sh all

# Run specific test types
./tools/testing/test-runner.sh unit
./tools/testing/test-runner.sh integration
./tools/testing/test-runner.sh api
./tools/testing/test-runner.sh coverage
./tools/testing/test-runner.sh lint
./tools/testing/test-runner.sh security

# Advanced options
./tools/testing/test-runner.sh all --report --verbose
./tools/testing/test-runner.sh unit --fast --clean
./tools/testing/test-runner.sh coverage --report

# Features:
# - Unit, integration, API, and security testing
# - Code coverage analysis with HTML reports
# - Performance benchmarking
# - Test artifact management
# - Parallel test execution
# - Detailed reporting and metrics
```

### 🔍 Linting Tools (`linting/`)

**Purpose**: Code quality, security, and style enforcement.

#### Professional Code Quality Suite
Enterprise-grade linting with comprehensive checks.

```bash
# Run all quality checks
./tools/linting/lint.sh

# Auto-format code
./tools/linting/format.sh

# Individual tools:
# - Flake8: Style and complexity analysis
# - Black: Code formatting
# - isort: Import organization
# - MyPy: Type checking
# - Bandit: Security vulnerability scanning
# - pydocstyle: Documentation standards
# - Pre-commit: Git hooks automation
```

## 🚀 Quick Start Guide

### 1. Initial Setup
```bash
# Set up development environment (one-time)
./tools/development/setup.sh

# Make all scripts executable
find tools/ -name "*.sh" -exec chmod +x {} \;
```

### 2. Daily Development Workflow
```bash
# Start development
./tools/development/dev-server.sh start

# Check code quality before commits
./tools/linting/lint.sh

# Run tests before pushing
./tools/testing/test-runner.sh unit --fast

# Monitor database health
./tools/database/health-check.sh
```

### 3. Pre-Deployment Validation
```bash
# Complete validation suite
./tools/testing/test-runner.sh all --report
./tools/linting/lint.sh
./tools/database/health-check.sh
```

## 📊 Tool Integration Features

### Cross-Tool Integration
- **Shared Configuration**: All tools use centralized `.env` configuration
- **Consistent Logging**: Unified colored output and logging format
- **Error Handling**: Graceful degradation and clear error messages
- **Report Generation**: Integrated reporting across all tools

### IDE Integration
- **VS Code Settings**: Automatic IDE configuration
- **Pre-commit Hooks**: Automatic quality checks on git commits
- **Live Feedback**: Real-time linting and formatting in editors

### CI/CD Ready
- **Exit Codes**: Proper exit codes for automation
- **Report Formats**: XML/JSON/HTML outputs for CI systems
- **Parallel Execution**: Optimized for build pipelines
- **Artifact Management**: Automated cleanup and archiving

## 🔧 Configuration Files

### Key Configuration Files
```
├── .env                     # Environment variables
├── .vscode/settings.json    # IDE configuration
├── .pre-commit-config.yaml  # Git hooks
├── pyproject.toml          # Python project configuration
├── pytest.ini             # Test configuration
├── tools/linting/          # Code quality configurations
│   ├── .flake8
│   ├── .bandit
│   └── .pydocstyle
└── docker-compose.yml      # Database services
```

### Environment Variables
```bash
# Application
DEBUG=true
SECRET_KEY=dev-secret-key
ENVIRONMENT=development

# Database
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5433/enrich_ddf_floor2
REDIS_URL=redis://localhost:6379/0

# External APIs
APOLLO_API_KEY=your_api_key
PEOPLEDATALABS_API_KEY=your_api_key
ZEROBOUNCE_API_KEY=your_api_key

# Testing
TESTING=false
LOG_LEVEL=DEBUG
```

## 📈 Monitoring and Metrics

### Health Check Metrics
- **Database Performance**: Query execution times
- **Memory Usage**: Redis and PostgreSQL memory consumption
- **Connection Health**: Active connections and pool status
- **Service Status**: Docker container health

### Test Metrics
- **Code Coverage**: Line and branch coverage analysis
- **Test Performance**: Execution time tracking
- **Quality Scores**: Linting and complexity metrics
- **Security Scanning**: Vulnerability detection

### Development Metrics
- **Build Times**: Dependency installation and setup times
- **Server Performance**: Startup and response times
- **Resource Usage**: CPU and memory monitoring

## 🛠️ Troubleshooting

### Common Issues

#### Environment Setup Problems
```bash
# Poetry not found
curl -sSL https://install.python-poetry.org | python3 -

# Python version issues
pyenv install 3.11.0
pyenv local 3.11.0

# Docker permission issues
sudo usermod -aG docker $USER
```

#### Database Connection Issues
```bash
# Start database services
docker-compose up -d db redis

# Check service status
docker-compose ps

# Reset database
docker-compose down -v
docker-compose up -d db redis
```

#### Test Failures
```bash
# Clean test artifacts
./tools/testing/test-runner.sh --clean

# Run with verbose output
./tools/testing/test-runner.sh unit --verbose

# Check specific test
poetry run pytest tests/unit/test_config.py -v
```

### Log Locations
```
├── dev-server.log          # Development server logs
├── test-reports/           # Test execution reports
│   ├── coverage/          # Coverage HTML reports
│   ├── unit-tests.xml     # JUnit test results
│   └── security-report.json # Security scan results
└── .coverage              # Coverage data
```

## 🔄 Tool Roadmap

### Phase 1: Core Development (✅ Completed)
- [x] Development environment automation
- [x] Code quality and linting
- [x] Testing framework
- [x] Database health monitoring

### Phase 2: Advanced Tooling (Planned)
- [ ] API documentation generation
- [ ] Performance profiling
- [ ] Load testing
- [ ] Deployment automation

### Phase 3: Production Tooling (Planned)
- [ ] Monitoring and alerting
- [ ] Backup and restore
- [ ] Security compliance
- [ ] Performance optimization

## 📚 Additional Resources

- **Tool Roadmap**: `tools/TOOLS_ROADMAP.md` - Complete tool ecosystem plan
- **Project Documentation**: `docs/` - Architecture and API documentation
- **Implementation Plans**: `docs/plans/active/` - Development roadmap

## 🤝 Contributing

When adding new tools:

1. **Follow Naming Conventions**: Use kebab-case for script names
2. **Add Documentation**: Update this README with new tool descriptions
3. **Include Help**: Add `--help` flag to all scripts
4. **Test Integration**: Ensure tools work with existing ecosystem
5. **Update Roadmap**: Add new tools to `TOOLS_ROADMAP.md`

---

**Enterprise Standards**: All tools follow enterprise development practices with proper error handling, logging, documentation, and integration capabilities. 