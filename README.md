# Enrich DDF Floor 2 - Unified Data Enrichment Platform

A comprehensive, production-ready data enrichment platform that aggregates and unifies all features from the DDF enrichment ecosystem without Streamlit dependencies.

## Repository Status

🚧 **In Development** - Initial setup complete, implementation in progress

## Quick Start

```bash
git clone https://github.com/dadosfera/enrich-ddf-floor-2.git
cd enrich-ddf-floor-2

# Install dependencies
pip install -r requirements-minimal.txt

# Setup pre-commit hooks
pre-commit install

# Run the application
./workflows/run.sh
```

## Development Setup

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

## Architecture

- **API-First**: FastAPI-based REST architecture
- **Non-Streamlit**: Production-ready without Streamlit dependencies
- **Unified Platform**: Aggregates all enrich-ddf-group features
- **Enterprise-Ready**: Docker, PostgreSQL, Redis, Celery

## Integrated Services

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

## Documentation

- **Guides**: [`docs/guides/`](docs/guides/)
- **Troubleshooting**: [`docs/troubleshooting/`](docs/troubleshooting/)
- **Lessons Learned**: [`docs/lessons_learned/`](docs/lessons_learned/)
