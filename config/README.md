# Configuration Package

This directory contains centralized configuration management for Enrich DDF Floor 2.

## Overview

The configuration package provides:
- **Port Configuration**: Centralized, environment-aware port allocation
- **Application Settings**: Environment-based configuration via Pydantic Settings
- **Linting Configuration**: Shared Ruff configuration

## Port Configuration (`ports.py`)

### Purpose

The `PortConfig` class provides centralized port management with environment-aware allocation. This eliminates hardcoded ports and prevents port conflicts during development.

### Key Features

- **Environment-aware**: Different port strategies for dev/staging/production
- **Random ports for dev**: Prevents port conflicts during development
- **Fixed ports for staging/production**: Predictable ports for deployment
- **No hardcoded localhost**: All URLs use `127.0.0.1` instead of `localhost`
- **No zeros in ports**: Production/staging ports don't contain zeros (8247, 8248, etc.)

### Port Allocation Strategy

| Environment | Backend Port | Frontend Port | Notes |
|------------|--------------|---------------|-------|
| **dev** | Random > 15000 | Random > 15000 | Prevents conflicts, different on each startup |
| **staging** | 8248 | 5174 | Fixed ports for staging environment |
| **production** | 8247 | 5173 | Fixed ports for production environment |

### Usage

```python
from config.ports import PortConfig

# Get ports for current environment
pc = PortConfig(environment="dev", host="127.0.0.1")
backend_port = pc.get_backend_port()  # Random port > 15000
frontend_port = pc.get_frontend_port()  # Random port > 15000

# Explicitly set ports (overrides automatic allocation)
pc.set_backend_port(9000)
pc.set_frontend_port(9001)
```

### Configuration

Ports can be configured via environment variables:

```bash
# Set environment (controls port allocation strategy)
export ENVIRONMENT=dev  # or staging, production

# Optionally override ports (bypasses PortConfig)
export PORT=9000
export FRONTEND_PORT=6000
```

Or via `.env` file:

```bash
ENVIRONMENT=dev
# PORT=9000  # Uncomment to override
# FRONTEND_PORT=6000  # Uncomment to override
```

### Integration

The `Settings` class in `config.py` automatically uses `PortConfig` when ports are not explicitly set, ensuring consistent port management across the application.

## Application Settings (`config.py`)

The root-level `config.py` file provides:
- Environment-based configuration via Pydantic Settings
- API key management
- Database configuration
- Security settings
- Integration with `PortConfig` for port management

### Usage

```python
from config import settings

# Access settings
port = settings.get_port()  # Uses PortConfig if not explicitly set
base_url = settings.get_base_url()  # Generates user-friendly URL
```

## Linting Configuration (`lint/`)

Shared Ruff configuration for consistent code quality across the project.

## Related Documentation

- [Port Configuration in README](../README.md#-port-configuration)
- [Port Management Architecture in ARCHITECTURE.md](../docs/ARCHITECTURE.md#-port-management-architecture)
- [Port Configuration Tests](../tests/unit/test_port_config.py)
- [Integration Tests](../tests/integration/test_port_config_startup.py)

## Design Decisions

### Why Centralized Port Configuration?

1. **Prevents Conflicts**: Random ports for dev prevent port conflicts
2. **Environment Consistency**: Same ports across staging/production
3. **No Hardcoded Values**: All ports managed through configuration
4. **Easy Override**: Environment variables allow easy customization

### Why No Zeros in Production Ports?

Production and staging ports (8247, 8248) don't contain zeros to avoid confusion and ensure clear identification in logs and monitoring.

### Why 127.0.0.1 Instead of localhost?

Using `127.0.0.1` instead of `localhost`:
- Avoids DNS resolution delays
- More explicit and reliable
- Consistent across platforms
- Better for containerized environments
