# Project Structure Guide

This document explains the directory structure and organization of the Enrich DDF Floor 2 codebase.

## 📁 Root Directory Structure

```
enrich-ddf-floor-2/
├── active/                    # Active plans and execution summaries
├── alembic/                   # Database migration files
├── config/                    # Configuration package
│   ├── ports.py              # Centralized port configuration
│   ├── __init__.py           # Package initialization
│   └── lint/                 # Shared linting configuration
├── core/                      # Core business logic
├── data/                      # Data layer (connectors, repositories)
├── database/                  # Database models and connection
├── deployment/                # Deployment configurations
├── docs/                      # Documentation
├── frontend/                  # React frontend application
├── guides/                    # Additional guides
├── prioritized/               # Prioritized tasks
├── services/                  # Service layer
├── templates/                 # Project templates
├── tests/                     # Test files
├── venv/                      # Python virtual environment (gitignored)
├── workflows/                 # Execution scripts
├── .pre-commit-config.yaml    # Pre-commit hooks configuration
├── alembic.ini                # Alembic configuration
├── compose.yml                # Docker Compose configuration
├── config.py                  # Application configuration
├── main.py                    # FastAPI application entry point
├── Makefile                   # Common commands
├── package.json               # Root package.json (if any)
├── pyproject.toml             # Python project configuration
├── README.md                  # Main README
└── requirements-minimal.txt   # Python dependencies
```

---

## 🎯 Canonical Taxonomy: Scripts & Workflows

**This section defines the authoritative rules for organizing scripts and workflows in this repository.**

### Scripts Organization

**Scripts belong under a top-level `scripts/{category}/` layout:**

- ✅ **Correct**: `scripts/quality/linter/`, `scripts/cost/`, `scripts/hooks/`
- ❌ **Forbidden**: Root-level `scripts/` directory (loose scripts at project root)

**Rationale**: Scripts are organized by category/domain. The taxonomy hook enforces that no root-level `scripts/` directory exists.

### Workflows Organization

**Workflows orchestrate scripts and live under `workflows/`:**

- **`workflows/run.sh`**: Main application entry point
- **`workflows/{category}/`**: Domain-specific workflow directories (e.g., `workflows/cost/`, `workflows/quality/`, `workflows/hooks/`)
- **`workflows/{category}/{workflow}/`**: Individual workflow implementations that may include workflow-local scripts

**Workflows orchestrate scripts from:**
- `scripts/{category}/` - Reusable script families organized by category
- `workflows/{category}/{workflow}/` - Workflow-specific scripts (if needed)

### Shared Utilities: `workflows/scripts/`

**`workflows/scripts/` is reserved for shared utilities and cross-repo tooling:**

- Cross-repository standardization tools (e.g., `bulk-update-repo.sh`)
- Shared infrastructure helpers (e.g., `detect_resources.sh`)
- Repository-level validation (e.g., `validate_taxonomy.py`)

**Important**: `workflows/scripts/` is **not** a primary home for domain scripts. Domain scripts belong in `scripts/{category}/` or within workflow-specific directories.

### Summary

| Location | Purpose | Example |
|----------|---------|---------|
| `scripts/{category}/` | Reusable script families organized by domain | `scripts/quality/linter/`, `scripts/cost/` |
| `workflows/{category}/` | Workflow orchestration by domain | `workflows/cost/`, `workflows/quality/` |
| `workflows/{category}/{workflow}/` | Workflow-specific scripts (if needed) | `workflows/cost/nightly-report/` |
| `workflows/scripts/` | Shared utilities and cross-repo tooling only | `workflows/scripts/validate_taxonomy.py` |

---

## 📂 Directory Details

### `/active/`

**Purpose**: Active plans and execution summaries

**Contents**:
- Execution summaries and reports
- Active development plans
- Status documents

**Example Files**:
- `73_repo_wide_resource_management_standardization.md`
- `74_intelligent_resource_adaptive_testing.md`
- `73_FINAL_EXECUTION_SUMMARY.md`

---

### `/alembic/`

**Purpose**: Database migration files

**Contents**:
- `env.py` - Alembic environment configuration
- `versions/` - Migration version files
- `script.py.mako` - Migration template

**Usage**:
```bash
# Create migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head
```

---

### `/core/`

**Purpose**: Core business logic

**Structure**:
```
core/
├── enrichment/           # Enrichment services
│   ├── company/          # Company enrichment logic
│   ├── contact/         # Contact enrichment logic
│   └── product/         # Product enrichment logic
├── integrations/        # External API integrations
└── utils/               # Utility functions
```

**Key Files**:
- `core/enrichment/real_data_enrichment.py` - Real data enrichment logic
- `core/enrichment/demo_enrichment.py` - Demo enrichment logic

---

### `/database/`

**Purpose**: Database models and connection management

**Structure**:
```
database/
├── __init__.py          # Package initialization
├── connection.py        # Database connection and session
├── models.py            # SQLAlchemy models
└── utils/               # Database utilities
```

**Key Files**:
- `connection.py` - Database engine and session management
- `models.py` - Company, Contact, Product models

---

### `/docs/`

**Purpose**: Project documentation

**Structure**:
```
docs/
├── analysis/            # Analysis documents
├── conversations/      # Conversation logs
├── guides/             # How-to guides
│   ├── cursor/         # Cursor-specific guides
│   └── ...
├── lessons_learned/    # Lessons learned
├── plans/              # Project plans
│   ├── active/        # Active plans
│   ├── backlog/       # Backlog items
│   ├── finished/      # Completed plans
│   └── prioritized/   # Prioritized plans
├── reports/            # Reports
├── status/             # Status documents
├── summaries/          # Summaries
├── troubleshooting/    # Troubleshooting guides
└── updates/           # Update notes
```

**Key Files**:
- `GETTING_STARTED.md` - Quick start guide
- `ARCHITECTURE.md` - Architecture documentation
- `PROJECT_STRUCTURE.md` - This file
- `TASKS_EXECUTED.md` - Completed tasks summary

---

### `/frontend/`

**Purpose**: React frontend application

**Structure**:
```
frontend/
├── public/              # Static assets
├── src/                 # Source code
│   ├── components/      # React components
│   │   └── common/      # Common UI components
│   ├── pages/           # Page components
│   ├── services/        # API service clients
│   ├── types/           # TypeScript types
│   ├── App.tsx          # Main app component
│   └── main.tsx         # Entry point
├── tests/               # Frontend tests
├── eslint.config.js     # ESLint configuration
├── package.json         # Frontend dependencies
├── tsconfig.json        # TypeScript configuration
└── vite.config.ts      # Vite configuration
```

**Key Files**:
- `src/App.tsx` - Main application component
- `src/pages/` - Page components (Dashboard, Companies, etc.)
- `src/services/` - API integration services

---

### `/workflows/scripts/`

**Purpose**: Shared utility scripts and cross-repo tooling

**Structure**:
```
workflows/scripts/
├── detect_resources.sh      # Resource detection helper
├── bulk-update-repo.sh      # Cross-repo standardization
├── validate_taxonomy.py     # Structure validation (pre-commit hook)
└── ...
```

**Key Scripts**:
- `detect_resources.sh` - Detect system resources
- `validate_taxonomy.py` - Validate project structure
- `bulk-update-repo.sh` - Update repository configuration
- `add-makefile-timeouts.sh` - Add timeouts to Makefile

---

### `/services/`

**Purpose**: Service layer

**Structure**:
```
services/
├── government_apis/     # Government API integrations
├── third_party/        # Third-party API clients
└── web_crawlers/       # Web crawling services
```

---

### `/tests/`

**Purpose**: Test files

**Structure**:
```
tests/
├── api_validation/     # API validation tests
├── e2e/                # End-to-end tests
├── integration/        # Integration tests
├── unit/               # Unit tests
├── conftest.py         # Pytest configuration
├── index_tests.yaml    # Test index
└── run_tests.sh        # Test runner script
```

**Test Organization**:
- `unit/` - Fast, isolated unit tests
- `integration/` - Integration tests with database
- `e2e/` - End-to-end tests with Playwright

---

### `/workflows/`

**Purpose**: Execution workflows and orchestration

**Structure**:
```
workflows/
├── run.sh          # Main application runner
├── cost/           # Cost management workflows
├── quality/        # Quality & linter governance workflows
├── hooks/          # Git hook tooling
└── scripts/        # Shared utility scripts (cross-repo tools, taxonomy, etc.)
```

**Key Files**:
- `run.sh` - Main application entry point with platform support

---

## 🔍 Key Files Explained

### Root Level Files

#### `main.py`
- FastAPI application entry point
- Route definitions
- Middleware configuration
- Application lifespan management

#### `/config/`

**Purpose**: Configuration package with centralized port management

**Structure**:
```
config/
├── ports.py              # Centralized port configuration (PortConfig class)
├── __init__.py           # Package initialization (exports settings and ports)
└── lint/                 # Shared linting configuration
    └── ruff-shared.toml  # Shared Ruff configuration
```

**Key Files**:
- `ports.py` - Environment-aware port allocation (dev/staging/production)
- `__init__.py` - Exports settings and ports modules for backward compatibility

**Usage**:
```python
from config.ports import PortConfig
from config import settings

# Get ports for current environment
pc = PortConfig(environment="dev", host="127.0.0.1")
backend_port = pc.get_backend_port()  # Random > 15000 for dev
```

**Related**: [Config Package README](../../config/README.md), [Port Configuration](../../README.md#-port-configuration)

---

#### `config.py`
- Application configuration using Pydantic Settings
- Environment variable management
- API key configuration
- Integration with PortConfig for port management

#### `Makefile`
- Common development commands
- Standardized targets across repos
- Timeout protection

#### `compose.yml`
- Docker Compose configuration
- Service definitions (backend, frontend)
- Resource limits and logging

#### `.pre-commit-config.yaml`
- Pre-commit hooks configuration
- Code quality checks
- Automated validation

#### `pyproject.toml`
- Python project configuration
- Ruff linting configuration
- Tool settings

---

## 📋 Naming Conventions

### Files

- **Python**: `snake_case.py` (e.g., `validate_taxonomy.py`)
- **TypeScript/React**: `PascalCase.tsx` (e.g., `App.tsx`)
- **Shell Scripts**: `kebab-case.sh` (e.g., `detect-resources.sh`)
- **Config Files**: `kebab-case.yml` (e.g., `compose.yml`)

### Directories

- **Lowercase with underscores**: `core/`, `database/`, `frontend/`
- **Plural for collections**: `services/`, `tests/`, `scripts/`

### Code

- **Python**: `snake_case` for functions/variables, `PascalCase` for classes
- **TypeScript**: `camelCase` for variables/functions, `PascalCase` for components/types

---

## 🚫 What Not to Commit

### Gitignored Files

- `venv/` - Python virtual environment
- `node_modules/` - Node.js dependencies
- `__pycache__/` - Python cache
- `*.pyc` - Compiled Python files
- `.env` - Environment variables (secrets)
- `*.log` - Log files
- `dist/` - Build outputs
- `.pytest_cache/` - Pytest cache
- `htmlcov/` - Coverage reports

---

## 🔄 Adding New Code

### Adding a New Feature

1. **Backend Feature**:
   ```
   core/
   └── enrichment/
       └── new_feature/
           ├── __init__.py
           └── service.py
   ```

2. **Frontend Feature**:
   ```
   frontend/src/
   ├── pages/
   │   └── NewFeature.tsx
   └── services/
       └── newFeatureService.ts
   ```

3. **Tests**:
   ```
   tests/
   └── unit/
       └── test_new_feature.py
   ```

### Adding a New Script

1. Create script in `scripts/`
2. Make executable: `chmod +x scripts/new_script.sh`
3. Document in `scripts/README.md`
4. Add to Makefile if commonly used

### Adding a New API Endpoint

1. Add route in `main.py`
2. Create service in `core/` or `services/`
3. Add database model if needed in `database/models.py`
4. Create migration: `alembic revision --autogenerate`
5. Add tests in `tests/api_validation/`

---

## 📖 Related Documentation

- [Getting Started Guide](./GETTING_STARTED.md)
- [Architecture Documentation](./ARCHITECTURE.md)
- [Contributing Guide](./CONTRIBUTING.md)
- [Scripts README](../workflows/scripts/README.md)

---

**Last Updated**: 2025-11-13
