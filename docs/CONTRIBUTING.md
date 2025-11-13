# Contributing Guide

Thank you for your interest in contributing to Enrich DDF Floor 2! This guide will help you get started.

## 🚀 Quick Start

1. **Fork the repository**
2. **Clone your fork**: `git clone https://github.com/your-username/enrich-ddf-floor-2.git`
3. **Create a branch**: `git checkout -b feature/your-feature-name`
4. **Make your changes**
5. **Test your changes**: `make test`
6. **Commit**: Follow [commit message conventions](#commit-messages)
7. **Push**: `git push origin feature/your-feature-name`
8. **Create Pull Request**

---

## 📋 Development Setup

### Prerequisites

- Python 3.11+
- Node.js 20+
- Git
- Pre-commit hooks (installed automatically)

### Setup Steps

```bash
# Clone repository
git clone https://github.com/dadosfera/enrich-ddf-floor-2.git
cd enrich-ddf-floor-2

# Install dependencies
make install

# Setup pre-commit hooks
pre-commit install

# Verify setup
make test
```

---

## 🧪 Testing

### Running Tests

```bash
# Run all tests
make test

# Run backend tests only
source venv/bin/activate
pytest

# Run frontend tests only
cd frontend && npm run lint

# Run with coverage
pytest --cov=. --cov-report=html
```

### Writing Tests

- **Unit Tests**: Fast, isolated tests in `tests/unit/`
- **Integration Tests**: Tests with database in `tests/integration/`
- **E2E Tests**: Full application tests in `tests/e2e/`

**Test Naming**:
- Python: `test_*.py` files, `test_*` functions
- TypeScript: `*.test.ts` or `*.spec.ts` files

**Example**:
```python
def test_create_company(db_session):
    company = Company(name="Test Corp", domain="test.com")
    db_session.add(company)
    db_session.commit()
    assert company.id is not None
```

---

## 📝 Code Style

### Python

- **Linter**: Ruff (configured in `pyproject.toml`)
- **Formatter**: Ruff (replaces Black)
- **Import Sorting**: Ruff (replaces isort)

**Format code**:
```bash
make format
# or
ruff format .
```

**Check linting**:
```bash
make lint
# or
ruff check .
```

### TypeScript/JavaScript

- **Linter**: ESLint (configured in `frontend/eslint.config.js`)
- **Formatter**: Prettier (via ESLint)

**Format code**:
```bash
cd frontend && npm run lint -- --fix
```

**Check linting**:
```bash
cd frontend && npm run lint
```

---

## 📦 Adding Dependencies

### Python Dependencies

1. Add to `requirements-minimal.txt`
2. Install: `pip install -r requirements-minimal.txt`
3. Update `requirements-minimal.txt` if version pinned

**Example**:
```bash
# Add new dependency
pip install new-package
pip freeze | grep new-package >> requirements-minimal.txt
```

### Node.js Dependencies

1. Add to `frontend/package.json`
2. Install: `cd frontend && npm install`
3. Commit `package-lock.json`

**Example**:
```bash
cd frontend
npm install new-package
```

---

## 🔀 Git Workflow

### Branch Naming

- **Features**: `feature/description` (e.g., `feature/add-user-auth`)
- **Bugfixes**: `fix/description` (e.g., `fix/port-conflict`)
- **Docs**: `docs/description` (e.g., `docs/update-readme`)
- **Refactor**: `refactor/description` (e.g., `refactor/api-structure`)

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding/updating tests
- `chore`: Maintenance tasks

**Examples**:
```
feat(api): add user authentication endpoint

Add POST /api/v1/auth/login endpoint with JWT token generation.

Closes #123
```

```
fix(database): resolve connection pool exhaustion

Increase pool size and add connection timeout handling.
```

---

## 🎯 Pull Request Process

### Before Submitting

- [ ] Code follows style guidelines
- [ ] All tests pass (`make test`)
- [ ] Linting passes (`make lint`)
- [ ] Documentation updated (if needed)
- [ ] Commit messages follow conventions
- [ ] No merge conflicts

### PR Checklist

- [ ] **Title**: Clear, descriptive title
- [ ] **Description**: Explain what and why
- [ ] **Tests**: Include test coverage
- [ ] **Documentation**: Update docs if needed
- [ ] **Breaking Changes**: Document if any
- [ ] **Related Issues**: Link related issues

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings
```

---

## 🏗️ Project Structure

Follow existing project structure:

- **Backend**: `core/`, `database/`, `services/`
- **Frontend**: `frontend/src/pages/`, `frontend/src/components/`
- **Tests**: `tests/unit/`, `tests/integration/`, `tests/e2e/`
- **Scripts**: `scripts/`

See [PROJECT_STRUCTURE.md](./PROJECT_STRUCTURE.md) for details.

---

## 🐛 Reporting Bugs

### Bug Report Template

```markdown
**Description**
Clear description of the bug

**Steps to Reproduce**
1. Step one
2. Step two
3. See error

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**Environment**
- OS: [e.g., macOS 14.0]
- Python: [e.g., 3.11.5]
- Node: [e.g., 20.10.0]
- Version: [e.g., 0.1.0]

**Additional Context**
Screenshots, logs, etc.
```

---

## 💡 Feature Requests

### Feature Request Template

```markdown
**Feature Description**
Clear description of the feature

**Use Case**
Why is this feature needed?

**Proposed Solution**
How should it work?

**Alternatives Considered**
Other approaches considered

**Additional Context**
Mockups, examples, etc.
```

---

## 🔍 Code Review Guidelines

### For Contributors

- **Be Responsive**: Respond to review comments promptly
- **Be Open**: Accept constructive feedback
- **Be Patient**: Reviews take time
- **Be Clear**: Explain your decisions

### For Reviewers

- **Be Constructive**: Provide helpful feedback
- **Be Respectful**: Use friendly, professional tone
- **Be Thorough**: Check functionality, style, tests
- **Be Timely**: Review within reasonable time

---

## 📚 Documentation

### When to Update Docs

- Adding new features
- Changing API endpoints
- Modifying configuration
- Adding new scripts
- Changing project structure

### Documentation Locations

- **User Docs**: `docs/guides/`
- **Architecture**: `docs/ARCHITECTURE.md`
- **API Docs**: Auto-generated at `/docs` endpoint
- **Code Comments**: Inline documentation

---

## 🚨 Security

### Reporting Security Issues

**DO NOT** open public issues for security vulnerabilities.

Instead:
1. Email security team directly
2. Include detailed description
3. Include steps to reproduce
4. Wait for response before disclosure

### Security Best Practices

- Never commit secrets or API keys
- Use environment variables for sensitive data
- Validate all user inputs
- Use parameterized queries (SQLAlchemy handles this)
- Keep dependencies updated

---

## ✅ Pre-commit Hooks

Pre-commit hooks run automatically on commit:

- **Ruff**: Python linting and formatting
- **Taxonomy Validation**: Project structure validation
- **YAML/JSON Validation**: Config file validation
- **Shellcheck**: Shell script linting
- **Commit Message**: Conventional commits validation

**Bypassing Hooks** (not recommended):
```bash
git commit --no-verify -m "message"
```

---

## 🎓 Learning Resources

### FastAPI
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)

### React
- [React Documentation](https://react.dev/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)

### SQLAlchemy
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)

### Testing
- [Pytest Documentation](https://docs.pytest.org/)
- [Playwright Documentation](https://playwright.dev/)

---

## 📞 Getting Help

- **Documentation**: Check `docs/` directory
- **Issues**: Check GitHub issues
- **Discussions**: GitHub Discussions (if enabled)
- **Code Review**: Ask in PR comments

---

## 🙏 Thank You!

Your contributions make this project better. Thank you for taking the time to contribute!

---

**Last Updated**: 2025-11-13
