#!/usr/bin/env python3
"""
Test script to debug FastAPI application loading
"""

from app.main import create_application

if __name__ == "__main__":
    app = create_application()
    
    print("=== Registered Routes ===")
    for route in app.routes:
        print(f"Path: {route.path}, Methods: {getattr(route, 'methods', 'N/A')}")
    
    print("\n=== Starting Test Server ===")
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 