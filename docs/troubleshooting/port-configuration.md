# Troubleshooting Port Configuration

This guide covers common issues with port configuration and their solutions.

## Common Issues

### 1. Port Already in Use Error

**Symptoms**:
```
OSError: [Errno 48] Address already in use
Port 8247 is already in use
```

**Root Cause**: The configured port is occupied by another process.

**Solution**:

**For Development Environment:**
- Development mode automatically uses random ports > 15000, which should prevent conflicts
- If conflicts occur, the system will automatically find an alternative port
- Check console output for the actual port being used

**For Staging/Production:**
```bash
# Check what's using the port
lsof -i :8247

# Kill the process if needed (be careful!)
kill -9 <PID>

# Or use a different port via environment variable
export PORT=9000
```

**Prevention**: Use development mode (`ENVIRONMENT=dev`) which uses random ports to prevent conflicts.

**Related**: [Port Configuration](../../README.md#-port-configuration), [Config Package README](../../config/README.md)

---

### 2. Frontend Cannot Connect to Backend

**Symptoms**:
- Frontend shows connection errors
- API calls fail with "ECONNREFUSED"
- Browser console shows network errors

**Root Cause**: Frontend is trying to connect to wrong backend port or backend is not running.

**Solution**:

1. **Verify backend is running**:
   ```bash
   # Check if backend process is running
   ps aux | grep "python.*main\|uvicorn"

   # Check what port backend is using
   lsof -i -P | grep LISTEN | grep python
   ```

2. **Set correct API URL**:
   ```bash
   # Get the actual backend port from console output
   # Then set VITE_API_URL environment variable
   export VITE_API_URL=http://127.0.0.1:<actual-port>

   # Restart frontend
   cd frontend && npm run dev
   ```

3. **Check environment variables**:
   ```bash
   # Verify VITE_API_URL is set correctly
   echo $VITE_API_URL
   ```

**Prevention**: Use centralized port configuration. The frontend automatically uses the correct port when `VITE_API_URL` is set.

**Related**: [Port Configuration](../../README.md#-port-configuration), [Frontend Configuration](../../frontend/README.md)

---

### 3. Port Configuration Not Working

**Symptoms**:
- Application uses wrong ports
- Environment variable `ENVIRONMENT` is ignored
- Ports don't match expected values

**Root Cause**: Port configuration not properly initialized or environment variable not set.

**Solution**:

1. **Verify environment variable**:
   ```bash
   # Check current environment
   echo $ENVIRONMENT

   # Set environment if not set
   export ENVIRONMENT=dev
   ```

2. **Test port configuration**:
   ```bash
   python3 -c "from config.ports import PortConfig; pc = PortConfig(environment='dev', host='127.0.0.1'); print(f'Backend: {pc.get_backend_port()}, Frontend: {pc.get_frontend_port()}')"
   ```

3. **Check config/ports.py is accessible**:
   ```bash
   # Verify file exists
   ls -la config/ports.py

   # Test import
   python3 -c "from config.ports import PortConfig; print('OK')"
   ```

4. **Verify Settings integration**:
   ```bash
   python3 -c "from config import settings; print(f'Port: {settings.get_port()}')"
   ```

**Prevention**: Always set `ENVIRONMENT` variable. Use `.env` file for consistent configuration.

**Related**: [Config Package README](../../config/README.md), [Environment Configuration](../../.env.example)

---

### 4. Random Ports Not Working in Dev Mode

**Symptoms**:
- Dev mode still uses fixed ports
- Ports are not > 15000
- Port conflicts occur

**Root Cause**: Environment not set to "dev" or PortConfig not being used.

**Solution**:

1. **Verify environment is set to dev**:
   ```bash
   export ENVIRONMENT=dev
   echo $ENVIRONMENT  # Should output "dev"
   ```

2. **Check application startup**:
   ```bash
   # Start with explicit environment
   ENVIRONMENT=dev bash workflows/run.sh --platform=local-macos --env=dev

   # Check console output for port numbers
   # Should see ports > 15000
   ```

3. **Verify PortConfig is being used**:
   ```bash
   # Test port allocation
   python3 -c "
   from config.ports import PortConfig
   pc = PortConfig(environment='dev', host='127.0.0.1')
   port = pc.get_backend_port()
   print(f'Port: {port}, > 15000: {port > 15000}')
   "
   ```

**Prevention**: Always set `ENVIRONMENT=dev` for development. Check console output to verify ports.

**Related**: [Port Configuration](../../README.md#-port-configuration), [Config Package README](../../config/README.md)

---

### 5. Docker Compose Port Conflicts

**Symptoms**:
- Docker containers fail to start
- Port binding errors
- Services cannot access each other

**Root Cause**: Port conflicts between host and container, or incorrect port mapping.

**Solution**:

1. **Check port availability**:
   ```bash
   # Check if ports are in use
   lsof -i :8247
   lsof -i :5173
   ```

2. **Set environment variables for Docker**:
   ```bash
   # Create .env file or export variables
   export ENVIRONMENT=production
   export BACKEND_PORT=8247
   export FRONTEND_PORT=5173

   # Start with compose
   docker compose --profile app up
   ```

3. **Verify port mappings in compose.yml**:
   ```yaml
   ports:
     - "${BACKEND_PORT:-8247}:${BACKEND_PORT:-8247}"
   ```

**Prevention**: Use environment variables in `compose.yml`. Set `ENVIRONMENT` variable appropriately.

**Related**: [Docker Compose Configuration](../../compose.yml), [Port Configuration](../../README.md#-port-configuration)

---

### 6. Import Error: Cannot Import PortConfig

**Symptoms**:
```
ImportError: cannot import name 'PortConfig' from 'config.ports'
ModuleNotFoundError: No module named 'config.ports'
```

**Root Cause**: `config/ports.py` file missing or Python path not set correctly.

**Solution**:

1. **Verify file exists**:
   ```bash
   ls -la config/ports.py
   ```

2. **Check Python path**:
   ```bash
   # Run from project root
   cd /path/to/enrich-ddf-floor-2
   python3 -c "from config.ports import PortConfig; print('OK')"
   ```

3. **Verify config/__init__.py exists**:
   ```bash
   ls -la config/__init__.py
   ```

4. **Reinstall if needed**:
   ```bash
   # If using virtual environment
   source venv/bin/activate
   pip install -e .
   ```

**Prevention**: Ensure `config/ports.py` is committed to repository. Run commands from project root.

**Related**: [Config Package README](../../config/README.md), [Project Structure](../PROJECT_STRUCTURE.md)

---

## General Troubleshooting Steps

### 1. Verify Port Configuration

```bash
# Test port allocation for each environment
python3 -c "
from config.ports import PortConfig

for env in ['dev', 'staging', 'production']:
    pc = PortConfig(environment=env, host='127.0.0.1')
    print(f'{env}: backend={pc.get_backend_port()}, frontend={pc.get_frontend_port()}')
"
```

### 2. Check Current Port Usage

```bash
# List all listening ports
lsof -i -P | grep LISTEN

# Check specific port
lsof -i :8247
lsof -i :5173
```

### 3. Verify Environment Variables

```bash
# Check all port-related environment variables
env | grep -E "(PORT|ENVIRONMENT|VITE_API)"

# Set if missing
export ENVIRONMENT=dev
export VITE_API_URL=http://127.0.0.1:8247
```

### 4. Test Port Availability

```bash
# Test if port is available
python3 -c "
from config.ports import is_port_available
print('Port 8247 available:', is_port_available(8247, '127.0.0.1'))
print('Port 15001 available:', is_port_available(15001, '127.0.0.1'))
"
```

## Getting Help

If issues persist:

1. **Check logs**: Review application startup logs for port allocation messages
2. **Verify configuration**: Check `.env` file and environment variables
3. **Test manually**: Run port configuration tests manually
4. **Review documentation**: See [Port Configuration](../../README.md#-port-configuration) and [Config Package README](../../config/README.md)

## Related Documentation

- [Port Configuration in README](../../README.md#-port-configuration)
- [Port Management Architecture](../ARCHITECTURE.md#-port-management-architecture)
- [Config Package README](../../config/README.md)
- [Port Configuration Tests](../../tests/unit/test_port_config.py)
- [Integration Tests](../../tests/integration/test_port_config_startup.py)
- [Lessons Learned: Centralized Port Configuration](../lessons_learned/2025-11-15_centralized-port-configuration.md)

---

**Last Updated**: 2025-11-15
