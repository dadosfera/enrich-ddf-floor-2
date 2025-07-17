#!/usr/bin/env python3
"""
Startup script for Enrich DDF Floor 2
"""

import uvicorn
from app.main import app

if __name__ == "__main__":
    print("Starting Enrich DDF Floor 2...")
    print("Web interface: http://localhost:8000")
    print("API docs: http://localhost:8000/docs")
    print("Health check: http://localhost:8000/health")
    print("Press Ctrl+C to stop")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    ) 