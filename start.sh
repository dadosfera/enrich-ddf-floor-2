#!/bin/bash

# Get the Poetry virtual environment path
VENV_PATH=$(poetry env info --path 2>/dev/null || echo "/tmp/poetry_cache/virtualenvs/enrich-ddf-floor-2-9TtSrW0h-py3.11")

# Activate Poetry virtual environment
if [ -f "$VENV_PATH/bin/activate" ]; then
    source "$VENV_PATH/bin/activate"
else
    echo "Virtual environment not found at $VENV_PATH"
    echo "Available environments:"
    poetry env list
    exit 1
fi

# Start the application
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload 