"""
FastAPI Application - Enrich DDF Floor 2
Main application module with API and web interface.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.api.v1.router import api_router
from app.web import router as web_router
from app.core.database import init_db, close_db, check_db_health
from app.core.logging import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    
    Handles startup and shutdown events.
    """
    # Startup
    setup_logging()
    await init_db()
    yield
    # Shutdown
    await close_db()


def create_application() -> FastAPI:
    """Create and configure the FastAPI application."""
    
    app = FastAPI(
        title="Enrich DDF Floor 2",
        description="Unified Data Enrichment Platform - Production Ready API",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    # Configure CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Mount static files
    static_dir = os.path.join(os.path.dirname(__file__), "static")
    if os.path.exists(static_dir):
        app.mount("/static", StaticFiles(directory=static_dir), name="static")
    
    # Include web interface routes first (for root route priority)
    app.include_router(web_router, tags=["web"])
    
    # Include API routes
    app.include_router(api_router, prefix="/api/v1", tags=["api"])
    
    # Add health check endpoint
    @app.get("/health")
    async def health_check():
        """Health check endpoint for load balancer."""
        db_healthy = await check_db_health()
        return {
            "status": "healthy" if db_healthy else "degraded",
            "service": "enrich-ddf-floor-2",
            "version": "0.1.0",
            "database": "connected" if db_healthy else "disconnected"
        }
    
    @app.get("/api/status")
    async def api_status():
        """API status endpoint."""
        return {
            "api_version": "v1",
            "status": "running",
            "features": {
                "authentication": "✅ Implemented",
                "web_interface": "✅ Implemented", 
                "database_layer": "✅ Implemented",
                "company_enrichment": "🔄 In Progress",
                "contact_enrichment": "🔄 In Progress",
                "product_classification": "🔄 In Progress",
                "multi_country_support": "🔄 In Progress"
            }
        }
    
    return app


# Create the application instance
app = create_application()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 