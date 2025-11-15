"""Enhanced FastAPI application for Enrich DDF Floor 2.

Provides database integration and dynamic port configuration.
"""

import logging
import os
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Any, Dict, List

import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from config import settings
from config.ports import PortConfig, get_user_friendly_url, is_port_available
from database.connection import Base, engine, get_db
from database.models import Company, Contact, Product


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Application lifespan manager."""
    # Startup
    print(f"🚀 Starting {settings.app_name} v{settings.app_version}")
    print(f"📊 Database: {settings.database_url}")
    print(f"🔒 Debug mode: {settings.debug}")

    # Create tables
    Base.metadata.create_all(bind=engine)

    yield

    # Shutdown
    print("🛑 Shutting down application...")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@app.get("/")
async def root():
    """Root endpoint returning basic application information."""
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.app_version,
        "status": "running",
        "debug": settings.debug,
        "docs_url": f"{settings.get_base_url()}/docs",
        "health_url": f"{settings.get_base_url()}/health",
    }


@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """Health check endpoint."""
    try:
        # Test database connection
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        logger.exception("Database health check failed")
        db_status = "disconnected"
        raise HTTPException(status_code=503, detail="Database unavailable") from e

    return {
        "status": "healthy",
        "version": settings.app_version,
        "database": db_status,
        "base_url": settings.get_base_url(),
        "timestamp": datetime.utcnow().isoformat(),
    }


@app.get("/api/v1/companies", response_model=List[Dict[str, Any]])
async def list_companies(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """List companies from database."""
    companies = db.query(Company).offset(skip).limit(limit).all()
    return [company.to_dict() for company in companies]


@app.post("/api/v1/companies", response_model=Dict[str, Any])
async def create_company(company_data: Dict[str, Any], db: Session = Depends(get_db)):
    """Create a new company."""
    try:
        company = Company(**company_data)
        db.add(company)
        db.commit()
        db.refresh(company)
        return {"status": "created", "id": company.id, "data": company.to_dict()}
    except Exception as e:
        db.rollback()
        logger.exception("Failed to create company")
        raise HTTPException(status_code=400, detail=str(e)) from e


@app.get("/api/v1/contacts", response_model=List[Dict[str, Any]])
async def list_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List contacts from database."""
    contacts = db.query(Contact).offset(skip).limit(limit).all()
    return [contact.to_dict() for contact in contacts]


@app.post("/api/v1/contacts", response_model=Dict[str, Any])
async def create_contact(contact_data: Dict[str, Any], db: Session = Depends(get_db)):
    """Create a new contact."""
    try:
        contact = Contact(**contact_data)
        db.add(contact)
        db.commit()
        db.refresh(contact)
        return {"status": "created", "id": contact.id, "data": contact.to_dict()}
    except Exception as e:
        db.rollback()
        logger.exception("Failed to create contact")
        raise HTTPException(status_code=400, detail=str(e)) from e


@app.get("/api/v1/products", response_model=List[Dict[str, Any]])
async def list_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List products from database."""
    products = db.query(Product).offset(skip).limit(limit).all()
    return [product.to_dict() for product in products]


@app.post("/api/v1/products", response_model=Dict[str, Any])
async def create_product(product_data: Dict[str, Any], db: Session = Depends(get_db)):
    """Create a new product."""
    try:
        product = Product(**product_data)
        db.add(product)
        db.commit()
        db.refresh(product)
        return {"status": "created", "id": product.id, "data": product.to_dict()}
    except Exception as e:
        db.rollback()
        logger.exception("Failed to create product")
        raise HTTPException(status_code=400, detail=str(e)) from e


if __name__ == "__main__":
    try:
        # Get environment from environment variable or settings
        environment = os.getenv("ENVIRONMENT", settings.environment)

        # Initialize port configuration
        port_config = PortConfig(environment=environment, host=settings.host)

        # Get ports from centralized configuration
        # If port is explicitly set in settings, use it; otherwise use PortConfig
        if settings.port is not None:
            available_port = settings.port
            port_config.set_backend_port(available_port)
        else:
            available_port = port_config.get_backend_port()

        # Verify port is available
        if not is_port_available(available_port, settings.host):
            logger.warning(f"Port {available_port} is occupied, finding alternative...")
            if environment == "dev":
                # For dev, get a new random port
                available_port = port_config.get_backend_port()
            else:
                # For staging/prod, try next available port
                from config.ports import find_available_port

                available_port = find_available_port(available_port, settings.host)
            logger.info(f"Using alternative port: {available_port}")

        # Get user-friendly URLs (convert 0.0.0.0 to 127.0.0.1 for browser access)
        backend_url = get_user_friendly_url(settings.host, available_port)
        frontend_port = settings.get_frontend_port_value()
        frontend_url = get_user_friendly_url(settings.frontend_host, frontend_port)

        # Log startup information with clear formatting
        print("\n" + "=" * 70)
        print("🚀 Enrich DDF Floor 2 - Application Starting")
        print("=" * 70)
        print(f"\n🌍 Environment: {environment}")
        print("\n📡 Backend API:")
        print(f"   • Base URL:     {backend_url}")
        print(f"   • API Docs:     {backend_url}/docs")
        print(f"   • Health Check: {backend_url}/health")
        print("\n🎨 Frontend:")
        print(f"   • Application:  {frontend_url}")
        print(
            f"\n💡 Tip: Open {frontend_url} in your browser to access the application"
        )
        print("=" * 70 + "\n")

        # Also log to logger for file logging
        logger.info(f"🌐 Server starting on {settings.host}:{available_port}")
        logger.info(f"🌍 Environment: {environment}")
        logger.info(f"📋 Backend URL: {backend_url}")
        logger.info(f"🎨 Frontend URL: {frontend_url}")
        logger.info(f"📚 API Docs: {backend_url}/docs")
        logger.info(f"❤️ Health Check: {backend_url}/health")

        uvicorn.run(
            "main:app",
            host=settings.host,
            port=available_port,
            reload=settings.debug,
            log_level=settings.log_level.lower(),
        )
    except Exception:
        logger.exception("Failed to start server")
        raise
