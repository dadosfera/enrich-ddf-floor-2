# AI Agent Guidelines - Enrich DDF Floor 2

## Application Startup Guidelines

### When Users Request to "Run the App"

**CRITICAL**: When a user asks to "run the app", "start the application", or similar requests, the AI agent should:

1. **DO NOT use timeout commands** - The user wants to validate the application themselves
2. **Start the application in the foreground** - Let the user see the startup logs and control the process
3. **Provide clear startup instructions** - Give the user the exact commands to run

### Correct Response Pattern

When users ask to run the application:

```bash
# ✅ CORRECT: Provide these commands to the user
source /Users/luismartins/local_repos/enrich-ddf-floor-2/venv/bin/activate
python main.py
```

**Expected Output:**
```
2025-07-29 17:56:30,640 - __main__ - INFO - 🌐 Server starting on 0.0.0.0:8247
2025-07-29 17:56:30,640 - __main__ - INFO - 📋 Base URL: http://0.0.0.0:8247
2025-07-29 17:56:30,640 - __main__ - INFO - 📚 API Docs: http://0.0.0.0:8247/docs
2025-07-29 17:56:30,640 - __main__ - INFO - ❤️ Health Check: http://0.0.0.0:8247/health
INFO:     Will watch for changes in these directories: ['/Users/luismartins/local_repos/enrich-ddf-floor-2']
INFO:     Uvicorn running on http://0.0.0.0:8247 (Press CTRL+C to quit)
INFO:     Started reloader process [19412] using WatchFiles
INFO:     Started server process [19536]
INFO:     Waiting for application startup.
🚀 Starting Enrich DDF Floor 2 v0.1.0
📊 Database: sqlite:///./app.db
🔒 Debug mode: True
INFO:     Application startup complete.
```

### What NOT to Do

❌ **DO NOT use timeout commands:**
```bash
# ❌ WRONG: This kills the app after 60 seconds
timeout 60 python main.py
```

❌ **DO NOT start in background:**
```bash
# ❌ WRONG: User can't see logs or control the process
python main.py &
```

### User Validation Process

After providing the startup commands, inform the user:

1. **The app will be accessible at**: `http://127.0.0.1:8247`
2. **Health check endpoint**: `http://127.0.0.1:8247/health`
3. **API documentation**: `http://127.0.0.1:8247/docs`
4. **To stop the app**: Press `Ctrl+C` in the terminal

### Port Configuration

- **Default port**: 8247 (non-round port to avoid conflicts)
- **Dynamic port detection**: If 8247 is occupied, app will use 8248, 8249, etc.
- **Configuration**: Port is set in `config.py`

### Testing Guidelines

When users want to test the application:

1. **Let them start the app themselves** - They need to see the startup process
2. **Provide validation endpoints** - Tell them what URLs to test
3. **Explain the expected behavior** - What they should see in the browser
4. **Don't use timeouts** - The app needs to run continuously

### Example User Interaction

**User**: "run the app"

**Agent Response**:
```
Please run the application with these commands:

```bash
source /Users/luismartins/local_repos/enrich-ddf-floor-2/venv/bin/activate
python main.py
```

The app will start on port 8247 and you can access it at:
- Main app: http://127.0.0.1:8247
- Health check: http://127.0.0.1:8247/health
- API docs: http://127.0.0.1:8247/docs

You'll see startup logs in the terminal. Press Ctrl+C to stop the app when you're done testing.
```

## General AI Agent Guidelines

### Command Execution Safety

- **Always use timeouts** for diagnostic commands (5-30 seconds)
- **Never use timeouts** for application startup when user requests it
- **Use background mode** only for long-running services that need to stay running
- **Provide clear instructions** to users for manual execution

### Port Management

- **Avoid hardcoded ports** - Use dynamic port detection
- **Use non-round ports** (8247 instead of 8000) to avoid conflicts
- **Check port availability** before starting services
- **Inform users** of the actual port being used

### User Experience

- **Let users control** application startup when they request it
- **Provide clear feedback** about what's happening
- **Explain expected behavior** and how to validate
- **Don't assume** users want background processes
