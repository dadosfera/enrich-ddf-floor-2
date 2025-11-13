# Enrich DDF Floor 2 - Unified Data Enrichment Platform

A comprehensive, production-ready data enrichment platform that aggregates and unifies all features from the DDF enrichment ecosystem without Streamlit dependencies.

## 🚀 Quick Start

**New to the project?** Start here: **[Getting Started Guide](docs/GETTING_STARTED.md)**

```bash
# Clone the repository
git clone https://github.com/dadosfera/enrich-ddf-floor-2.git
cd enrich-ddf-floor-2

# Install all dependencies
make install

# Setup pre-commit hooks
pre-commit install

# Run the application
make run
```

**The application will be available at:**
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8247
- **API Documentation**: http://localhost:8247/docs

## 📚 Documentation

### For Newcomers
- **[Getting Started Guide](docs/GETTING_STARTED.md)** - Complete setup and first steps
- **[Architecture Documentation](docs/ARCHITECTURE.md)** - System design and components
- **[Project Structure](docs/PROJECT_STRUCTURE.md)** - Directory layout explained
- **[Tasks Executed](docs/TASKS_EXECUTED.md)** - Summary of completed work

### For Developers
- **[Contributing Guide](docs/CONTRIBUTING.md)** - How to contribute
- **[Quick Reference](docs/guides/QUICK_REFERENCE.md)** - Common commands and workflows
- **[Troubleshooting](docs/troubleshooting/)** - Solutions to common issues

### Additional Resources
- **[Guides](docs/guides/)** - How-to guides and tutorials
- **[Plans](docs/plans/)** - Project plans and roadmaps
- **[Reports](docs/reports/)** - Status reports and analysis

## 🛠️ Common Commands

| Command | Description |
|---------|-------------|
| `make run` | Start both frontend and backend |
| `make backend` | Start only backend server |
| `make frontend` | Start only frontend server |
| `make test` | Run all tests |
| `make lint` | Run linting checks |
| `make format` | Format code automatically |
| `make install` | Install all dependencies |
| `make clean` | Clean build artifacts |

See [Getting Started Guide](docs/GETTING_STARTED.md#common-commands) for more commands.

## 🏗️ Architecture

- **API-First**: FastAPI-based REST architecture
- **Frontend**: React + TypeScript + Vite
- **Database**: SQLAlchemy + SQLite (dev) / PostgreSQL (prod)
- **Non-Streamlit**: Production-ready without Streamlit dependencies
- **Unified Platform**: Aggregates all enrich-ddf-group features
- **Enterprise-Ready**: Docker, PostgreSQL, Redis, Celery (planned)

For detailed architecture information, see [Architecture Documentation](docs/ARCHITECTURE.md).

## 🔌 Integrated Services

Consolidates features from:

1. **enrich-ddf**: Multi-country company data platform
2. **dataapp-enriching**: Contact enrichment with deduplication
3. **data-app-alpha-enrichment**: Alpha enrichment components
4. **dataapp-enriquecimento**: People data enrichment
5. **enrich-ddf-mod-ncm**: NCM product classification

## Code Quality & Standards

### Linting & Formatting

This project uses **Ruff** for all Python linting and formatting:

- **Linting**: Replaces flake8, pylint, pycodestyle, and more
- **Formatting**: Replaces Black
- **Import Sorting**: Replaces isort (via Ruff's `I` rule)

**Configuration:**

- Main config: [`pyproject.toml`](pyproject.toml)
- Pre-commit hooks: [`.pre-commit-config.yaml`](.pre-commit-config.yaml)

**Migration History:**

- ✅ Migrated from Black + isort to Ruff-only (2025-01-27)
- ✅ Eliminated tool conflicts and improved performance
- ✅ See [Migration Guide](docs/lessons_learned/2025-01-27_ruff-migration.md) for details

### Project Structure Validation

The `scripts/validate_taxonomy.py` script ensures project structure compliance:

- Validates required directories exist
- Prevents invalid directory names (e.g., `-copy`, `-backup`, `-partial`)
- Runs automatically via pre-commit hooks

See [Scripts Documentation](scripts/README.md) for more details.

## 🔧 Development Setup

### Pre-commit Hooks

This repository uses [pre-commit](https://pre-commit.com/) to ensure code quality before commits. The hooks are automatically installed when you run `pre-commit install`.

**Current Setup:**

- **Ruff** (linting and formatting) - Replaces Black, isort, flake8, and more
- **Taxonomy validation** - Ensures project structure compliance
- **YAML/JSON validation** - Validates configuration files
- **Shell script linting** - Checks shell scripts with shellcheck
- **Commit message validation** - Enforces conventional commits

**Key Features:**

- ✅ **Ruff-only setup**: Modern, fast Python linting and formatting
- ✅ **No conflicts**: Single tool handles all Python code quality
- ✅ **Fast execution**: Ruff is 10-100x faster than traditional tools

For detailed configuration, see:

- [Pre-commit Configuration](.pre-commit-config.yaml)
- [Ruff Configuration Guide](docs/guides/cursor/isort-ruff-configuration-guide.md)
- [Troubleshooting Pre-commit Hooks](docs/troubleshooting/pre-commit-hooks.md)

## 📊 Project Status

🚧 **In Development** - Initial setup complete, implementation in progress

**Recent Achievements:**
- ✅ Resource management standardization across 30+ repos
- ✅ Intelligent adaptive testing system
- ✅ Database integration complete
- ✅ Frontend application running
- ✅ API endpoints functional
- ✅ 96.12% test coverage

See [Tasks Executed](docs/TASKS_EXECUTED.md) for complete summary.

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](docs/CONTRIBUTING.md) for details.

**Quick Contribution Steps:**
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`make test`)
5. Commit your changes (`git commit -m 'feat: add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📖 Additional Documentation

- **Guides**: [`docs/guides/`](docs/guides/)
- **Troubleshooting**: [`docs/troubleshooting/`](docs/troubleshooting/)
- **Lessons Learned**: [`docs/lessons_learned/`](docs/lessons_learned/)
- **Plans**: [`docs/plans/`](docs/plans/)
- **Reports**: [`docs/reports/`](docs/reports/)
