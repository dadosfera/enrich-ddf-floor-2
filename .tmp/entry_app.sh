#!/bin/bash
set -e
if [ ! -f /app/.venv/bin/activate ]; then
  echo "[ERROR] /app/.venv/bin/activate not found. Poetry venv not created!"
  ls -l /app/.venv || true
  exit 1
fi
source /app/.venv/bin/activate
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
