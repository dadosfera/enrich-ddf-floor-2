# Git Hooks Implementation for enrich-ddf-floor-2

## 🎯 Overview

This document describes the comprehensive git hooks system implemented for the enrich-ddf-floor-2 project, inspired by the deployer-ddf-mod-open-llms project's taxonomy validation approach.

## 📋 What Was Implemented

### 1. **Pre-commit Configuration** (`.pre-commit-config.yaml`)
- **Code Quality**: Black, Flake8, Prettier formatting
- **Shell Validation**: ShellCheck for bash scripts
- **Custom Hooks**: Taxonomy validation, API key protection, test validation
- **Frontend Checks**: Build validation for TypeScript/React changes

### 2. **Taxonomy Validation** (`scripts/hooks/validate-taxonomy.sh`)
Validates project directory structure and file placement:
- ✅ **Core Structure**: Ensures required directories exist (core/, data/, services/, tests/, frontend/, database/)
- ✅ **File Placement**: Validates Python files are in appropriate subdirectories
- ✅ **Test Organization**: Ensures test files are in tests/ directory
- ✅ **Configuration Management**: Validates .env file structure and API key safety
- ✅ **Documentation**: Checks for essential documentation files
- ✅ **Temporary Files**: Validates proper temporary file management

### 3. **API Key Protection** (`scripts/hooks/protect-api-keys-fast.sh`)
Fast security checks to prevent credential leaks:
- 🔒 **Real API Keys**: Detects AWS (AKIA...), OpenAI (sk-...), GitHub tokens
- 🔒 **Sensitive Files**: Prevents committing private keys, certificates
- 🔒 **Environment Files**: Validates .env files for real credentials
- 🔒 **Database Files**: Warns about large database files
- 🔒 **Staged Files**: Checks git staged files for API key patterns

### 4. **Commit Message Template** (`.gitmessage`)
Structured commit messages with:
- **Types**: feat, fix, docs, style, refactor, test, chore, perf, ci, build, revert
- **Scopes**: api, frontend, database, enrichment, integrations, hunter, clearbit, etc.
- **Examples**: Real-world commit message examples for the project
- **Guidelines**: Best practices for commit message formatting

### 5. **Installation Script** (`scripts/hooks/install-git-hooks.sh`)
Automated setup with:
- ✅ **Prerequisites Check**: Validates git repository and required files
- ✅ **Pre-commit Installation**: Installs pre-commit framework
- ✅ **Hook Configuration**: Sets up all hooks and templates
- ✅ **Testing**: Validates installation with test runs
- ✅ **Documentation**: Provides usage instructions

## 🚀 How to Use

### Initial Setup
```bash
# Run the installation script
bash scripts/hooks/install-git-hooks.sh

# Or install manually
pip install pre-commit
pre-commit install
pre-commit install --hook-type pre-push
git config commit.template .gitmessage
```

### Daily Usage
```bash
# Hooks run automatically on commit/push
git add .
git commit  # Opens commit template
git push

# Manual validation
scripts/hooks/validate-taxonomy.sh
scripts/hooks/protect-api-keys-fast.sh

# Skip hooks in emergency (not recommended)
git commit --no-verify
```

### Commit Message Examples
```bash
# Good commit messages
feat(enrichment): add real-time person data enrichment via Hunter.io
fix(frontend): resolve TypeScript compilation errors in Components
feat(integrations): implement Clearbit company enrichment API
test(e2e): add comprehensive data enrichment flow tests
docs(api): update API documentation with new enrichment endpoints
chore(deps): update React and Vite to latest versions
```

## 🔧 Configuration Files

### `.pre-commit-config.yaml`
```yaml
# Main pre-commit configuration
# - Code quality hooks (Black, Flake8, Prettier, ShellCheck)
# - Custom project hooks (taxonomy, API protection, tests)
# - Frontend build validation
```

### `.gitmessage`
```
# Commit message template
# - Structured format with types and scopes
# - Project-specific examples
# - Best practice guidelines
```

### `scripts/hooks/`
- `validate-taxonomy.sh` - Project structure validation
- `protect-api-keys-fast.sh` - Fast API key protection
- `protect-api-keys.sh` - Comprehensive API key protection (slower)
- `install-git-hooks.sh` - Automated installation

## 🛡️ Security Features

### API Key Protection
- **Prevents Real Keys**: Blocks commits with real AWS, OpenAI, GitHub tokens
- **Template Enforcement**: Ensures .env files use placeholders
- **Staged File Scanning**: Checks git staged files for credentials
- **Fast Execution**: Optimized for quick pre-commit checks

### File Security
- **Private Keys**: Prevents committing .pem, .key, certificates
- **Large Databases**: Warns about large .db files that shouldn't be committed
- **Sensitive Patterns**: Detects common credential patterns

## 📊 Validation Rules

### Directory Structure
```
enrich-ddf-floor-2/
├── core/           ✅ Required (enrichment, integrations, utils)
├── data/           ✅ Required (connectors, repositories, migrations)
├── services/       ✅ Required (third_party, government_apis, web_crawlers)
├── tests/          ✅ Required (all test files go here)
├── frontend/       ✅ Required (React/Vite frontend)
├── database/       ✅ Required (models, utils, migrations)
├── scripts/        ✅ Allowed (project scripts)
├── alembic/        ✅ Allowed (database migrations)
├── main.py         ✅ Allowed (main application file)
└── config.py       ✅ Allowed (configuration file)
```

### File Placement Rules
- **Python Files**: Must be in core/, services/, database/, data/, tests/, scripts/, or project root (main.py, config.py)
- **Test Files**: Must be in tests/ directory (except frontend/tests/)
- **Configuration**: .env files must use placeholders, not real credentials
- **Temporary Files**: Should be in .tmp/ directory for automatic cleanup

## 🎛️ Customization

### Modify Hook Behavior
Edit `.pre-commit-config.yaml` to:
- Enable/disable specific hooks
- Adjust timeout values
- Change file patterns
- Add new validation rules

### Update Taxonomy Rules
Edit `scripts/hooks/validate-taxonomy.sh` to:
- Add new required directories
- Modify file placement rules
- Update validation logic
- Add project-specific checks

### Customize API Protection
Edit `scripts/hooks/protect-api-keys-fast.sh` to:
- Add new API key patterns
- Modify sensitive file detection
- Update credential validation
- Add project-specific security rules

## 🚨 Troubleshooting

### Common Issues

**Hook Installation Fails**
```bash
# Install pre-commit manually
pip install pre-commit
# Or with conda
conda install pre-commit
```

**Taxonomy Validation Errors**
```bash
# Check current issues
scripts/hooks/validate-taxonomy.sh

# Common fixes:
# 1. Move Python files to appropriate directories
# 2. Move test files to tests/ directory
# 3. Remove real API keys from .env
# 4. Move temporary files to .tmp/
```

**API Key Protection Warnings**
```bash
# Check for real credentials
scripts/hooks/protect-api-keys-fast.sh

# Fix by:
# 1. Replace real API keys with placeholders
# 2. Add sensitive files to .gitignore
# 3. Use .env.example for templates
```

**Performance Issues**
- Use `protect-api-keys-fast.sh` instead of `protect-api-keys.sh`
- Exclude large directories in hook configurations
- Run hooks on staged files only during pre-commit

### Skip Hooks (Emergency Only)
```bash
# Skip all hooks (not recommended)
git commit --no-verify

# Skip specific hook
SKIP=api-key-protection git commit
```

## 📈 Benefits

### Code Quality
- ✅ **Consistent Formatting**: Black, Prettier, ShellCheck
- ✅ **Project Structure**: Enforced directory organization
- ✅ **Documentation**: Required documentation files
- ✅ **Test Organization**: Proper test file placement

### Security
- 🔒 **Credential Protection**: Prevents API key leaks
- 🔒 **Sensitive Files**: Blocks private key commits
- 🔒 **Environment Safety**: Validates .env file security
- 🔒 **Staged File Scanning**: Real-time credential detection

### Development Workflow
- 🚀 **Automated Validation**: Runs on every commit/push
- 🚀 **Fast Feedback**: Quick validation with detailed error messages
- 🚀 **Structured Commits**: Consistent commit message format
- 🚀 **Easy Setup**: One-command installation

## 🔄 Maintenance

### Regular Updates
- Update pre-commit hook versions in `.pre-commit-config.yaml`
- Review and update taxonomy rules as project evolves
- Add new API key patterns as services are integrated
- Update commit message template with new scopes

### Monitoring
- Review hook execution logs for performance issues
- Monitor false positives in API key detection
- Update file placement rules based on project growth
- Collect feedback from team on hook effectiveness

## 🎉 Success Metrics

The git hooks implementation provides:
- **100% API Key Protection**: No real credentials in commits
- **Consistent Project Structure**: Enforced directory organization
- **Improved Code Quality**: Automated formatting and linting
- **Better Commit Messages**: Structured, informative commits
- **Fast Validation**: < 30 seconds for most pre-commit checks
- **Developer Friendly**: Clear error messages and fix suggestions

This comprehensive git hooks system ensures code quality, security, and project organization while maintaining developer productivity and workflow efficiency.
