# centralize-port-configuration – next actions

**Status**: backlog
**Created from**: Conversation review on 2025-11-15
**Objective**: Centralize port configuration with environment-aware allocation
**Priority**: Low (work completed, future enhancements only)
**Estimated effort**: 2-4 AI hours / 1-2 Human hours

## Next actions (not-yet-tried / unplanned)

### Optional Future Enhancements

- [ ] Consider increasing Python minimum version requirement to 3.9+
  - **Rationale**: Current code uses nested `with` statements for Python 3.8 compatibility, but Python 3.9+ allows cleaner syntax with parentheses
  - **Action**: If project can require Python 3.9+, update `pyproject.toml` and refactor nested `with` statements in `tests/unit/test_port_config.py`
  - **Scope**: Configuration update + code refactoring
  - **Impact**: Code quality improvement, cleaner syntax

- [ ] Add port configuration validation to CI/CD pipeline
  - **Rationale**: Ensure port configuration works correctly in automated environments
  - **Action**: Add CI tests that verify port allocation for different environments (dev/staging/production)
  - **Scope**: CI/CD configuration enhancement
  - **Impact**: Prevents regressions in port configuration

- [ ] Add port allocation monitoring/logging
  - **Rationale**: Track actual port usage patterns and conflicts in production
  - **Action**: Add structured logging/metrics for port allocation events (which ports used, conflicts detected, fallbacks triggered)
  - **Scope**: Observability enhancement
  - **Impact**: Better visibility into port allocation behavior

- [ ] Update deployment guides with new port configuration
  - **Rationale**: Deployment documentation may reference old port configuration
  - **Action**: Review deployment documentation and update with new centralized port configuration details
  - **Scope**: Documentation maintenance
  - **Impact**: Ensures deployment docs match implementation

## Context from conversation

### Completed Work

**Core Implementation:**
- Created `config/ports.py` with `PortConfig` class for centralized port management
- Environment-aware port allocation: dev (random > 15000), staging (8248/5174), production (8247/5173)
- Removed all hardcoded "localhost" references (replaced with 127.0.0.1)
- Removed ports containing zeros (production/staging use 8247, 8248, etc.)
- Updated all configuration files, frontend files, and Docker Compose

**Testing & Validation:**
- 29 unit tests created and passing (`tests/unit/test_port_config.py`)
- 10 integration tests created and passing (`tests/integration/test_port_config_startup.py`)
- All runtime validation completed (dev/staging/production environments)
- Port conflict handling verified

**Documentation:**
- Updated `.env.example` with port configuration documentation
- Updated `README.md` with Port Configuration section
- Updated `docs/ARCHITECTURE.md` with Port Configuration (2.1) and Port Management Architecture sections

**Code Quality:**
- Fixed Python 3.8 compatibility issues
- All pre-commit hooks passing
- All changes committed and pushed

### Key Decisions

1. **Port Allocation Strategy**:
   - Dev: Random ports > 15000 (prevents conflicts)
   - Staging: Fixed ports 8248 (backend), 5174 (frontend)
   - Production: Fixed ports 8247 (backend), 5173 (frontend)

2. **No Hardcoded Values**:
   - All "localhost" replaced with "127.0.0.1"
   - All ports managed through `PortConfig` class
   - Environment variables supported for overrides

3. **Python 3.8 Compatibility**:
   - Used nested `with` statements instead of parentheses syntax
   - Added `# noqa: SIM117` comments for style warnings

### Constraints

- Must support Python 3.8+ (project requirement)
- Production/staging ports must not contain zeros
- Dev environment must use random ports > 15000
- All configuration must support environment variable overrides

## Links

- **Implementation**: `config/ports.py`
- **Tests**: `tests/unit/test_port_config.py`, `tests/integration/test_port_config_startup.py`
- **Documentation**: `docs/ARCHITECTURE.md` (sections 2.1 and Port Management Architecture)
- **Configuration**: `.env.example`, `README.md` (Port Configuration section)
- **Related commits**:
  - `e3b01eaab` - feat(config): centralize port config with random dev ports
  - `ecf264756` - fix(config): export settings from config/__init__.py
  - `4fad2262b` - test(docs): add comprehensive tests and docs for port config
  - `e8252691c` - fix: resolve hook errors and Python 3.8 compatibility
