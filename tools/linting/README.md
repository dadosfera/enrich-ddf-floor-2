# Professional Linting Suite - Enrich DDF Floor 2

This directory contains a comprehensive, enterprise-grade linting and code quality configuration for the Enrich DDF Floor 2 project.

## 🎯 Overview

Our linting suite ensures:
- **Code Quality**: Consistent, readable, and maintainable code
- **Security**: Automated vulnerability scanning
- **Type Safety**: Static type checking with mypy
- **Documentation**: Proper docstring standards
- **Performance**: Optimized imports and code structure

## 📁 Directory Structure

```
tools/linting/
├── README.md                    # This documentation
├── .flake8                      # Flake8 linting configuration
├── .bandit                      # Bandit security scanning config
├── .pydocstyle                  # Documentation style config
├── .pre-commit-config.yaml      # Pre-commit hooks configuration
├── pyproject.toml               # Black, isort, mypy, pytest config
├── lint.sh                      # Main linting script
└── format.sh                    # Auto-formatting script
```

## 🛠️ Tools Included

| Tool | Purpose | Configuration |
|------|---------|---------------|
| **Black** | Code formatting | `pyproject.toml` |
| **isort** | Import sorting | `pyproject.toml` |  
| **flake8** | Style & error checking | `.flake8` |
| **mypy** | Type checking | `pyproject.toml` |
| **bandit** | Security scanning | `.bandit` |
| **pydocstyle** | Documentation style | `.pydocstyle` |
| **pre-commit** | Git hooks | `.pre-commit-config.yaml` |

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Install development dependencies
poetry install --with dev

# Install pre-commit hooks
poetry run pre-commit install
```

### 2. Run Linting

```bash
# Check code quality (read-only)
./tools/linting/lint.sh

# Auto-fix formatting issues
./tools/linting/format.sh
```

### 3. IDE Integration

#### VS Code / Cursor
Add to your `.vscode/settings.json`:

```json
{
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "python.linting.flake8Args": ["--config=tools/linting/.flake8"],
  "python.formatting.provider": "black",
  "python.formatting.blackArgs": ["--config=tools/linting/pyproject.toml"],
  "python.sortImports.args": ["--settings-path=tools/linting/pyproject.toml"],
  "python.linting.mypyEnabled": true,
  "python.linting.mypyArgs": ["--config-file=tools/linting/pyproject.toml"]
}
```

## 📋 Linting Standards

### Code Style
- **Line Length**: 88 characters (Black standard)
- **Indentation**: 4 spaces
- **Quotes**: Double quotes preferred
- **Import Order**: stdlib → third-party → first-party → local

### Type Annotations
- Required for all public functions
- Return types must be specified
- Use `typing` module for complex types

### Documentation
- Google-style docstrings
- All public functions and classes must have docstrings
- Docstrings should include Args, Returns, and Raises sections

### Security
- No hardcoded passwords or API keys
- Safe subprocess usage
- Input validation for user data

## 🔧 Scripts Usage

### `lint.sh` - Comprehensive Linting

Runs all linting tools in sequence:

```bash
./tools/linting/lint.sh
```

**Output**: Detailed report with pass/fail status for each tool.

**Exit Codes**:
- `0`: All checks passed
- `1`: One or more checks failed

### `format.sh` - Auto-formatting

Automatically fixes code style issues:

```bash
./tools/linting/format.sh
```

**Actions**:
1. Removes unused imports (autoflake)
2. Sorts imports (isort)
3. Formats code (Black)
4. Removes trailing whitespace
5. Fixes PEP8 issues (autopep8)

## 🔗 Pre-commit Integration

Pre-commit hooks run automatically on `git commit`:

```bash
# Install hooks
poetry run pre-commit install

# Run manually on all files
poetry run pre-commit run --all-files

# Skip hooks for emergency commits
git commit --no-verify -m "Emergency fix"
```

## 📊 Quality Metrics

Our linting suite enforces:

- **Code Coverage**: Minimum 80%
- **Complexity**: Maximum 10 (McCabe)
- **Type Coverage**: 100% for public APIs
- **Documentation**: All public functions documented
- **Security**: Zero high-severity vulnerabilities

## 🛡️ Security Scanning

Bandit scans for common security issues:

```bash
# Run security scan
poetry run bandit -r app/ -c tools/linting/.bandit

# Generate detailed report
poetry run bandit -r app/ -f json -o security-report.json
```

## 🔍 Type Checking

MyPy ensures type safety:

```bash
# Run type checking
poetry run mypy --config-file=tools/linting/pyproject.toml app/

# Generate coverage report
poetry run mypy --config-file=tools/linting/pyproject.toml --html-report mypy-report app/
```

## 🎯 CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/lint.yml
name: Lint
on: [push, pull_request]
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install poetry
      - run: poetry install --with dev
      - run: ./tools/linting/lint.sh
```

### Docker Integration

```dockerfile
# Add to Dockerfile for production builds
COPY tools/linting tools/linting
RUN ./tools/linting/lint.sh
```

## 🔧 Customization

### Adding New Rules

1. **flake8**: Edit `.flake8` → `select` section
2. **mypy**: Edit `pyproject.toml` → `[tool.mypy]`
3. **bandit**: Edit `.bandit` → `tests` section

### Project-Specific Ignores

```ini
# .flake8 - Per-file ignores
per-file-ignores =
    your_file.py:E501,F401
    tests/*:S101
```

### IDE-Specific Settings

Create `.vscode/settings.json`, `.idea/`, or equivalent for your IDE.

## 📚 References

- [Black Documentation](https://black.readthedocs.io/)
- [flake8 Error Codes](https://flake8.pycqa.org/en/latest/user/error-codes.html)
- [mypy Configuration](https://mypy.readthedocs.io/en/stable/config_file.html)
- [Bandit Security Tests](https://bandit.readthedocs.io/en/latest/tests/index.html)
- [Pre-commit Hooks](https://pre-commit.com/hooks.html)

## 🆘 Troubleshooting

### Common Issues

**Poetry not found**:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

**Permission denied on scripts**:
```bash
chmod +x tools/linting/*.sh
```

**Tool not installed**:
```bash
poetry install --with dev
```

**Pre-commit failing**:
```bash
poetry run pre-commit clean
poetry run pre-commit install
```

---

**Maintained by**: Enrich DDF Development Team  
**Last Updated**: June 2025  
**Version**: 1.0.0 