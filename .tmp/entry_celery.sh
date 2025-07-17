#!/bin/bash
set -e
if [ ! -f /app/.venv/bin/activate ]; then
  echo "[ERROR] /app/.venv/bin/activate not found. Poetry venv not created!"
  ls -l /app/.venv || true
  exit 1
fi
source /app/.venv/bin/activate
exec celery -A app.core.celery worker --loglevel=info
