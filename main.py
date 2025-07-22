"""Enhanced FastAPI application for Enrich DDF Floor 2.

Provides database integration and dynamic port configuration.
"""

import logging
import socket
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Any, Dict, List

import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from config import settings
from database.connection import Base, engine, get_db
from database.models import Company, Contact, Product


def is_port_available(port: int, host: str = "localhost") -> bool:
    """Check if a port is available for binding."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex((host, port))
            return result != 0
    except Exception:
        return False


def find_available_port(
    start_port: int, host: str = "localhost", max_attempts: int = 10
) -> int:
    """Find an available port starting from start_port."""
    for i in range(max_attempts):
        port = start_port + i
        if is_port_available(port, host):
            return port
    raise RuntimeError(
        f"No available port found in range "
        f"{start_port}-{start_port + max_attempts - 1}"
    )


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
    # Find available port if configured port is occupied
    try:
        if not is_port_available(settings.port, settings.host):
            logger.warning(f"Port {settings.port} is occupied, finding alternative...")
            available_port = find_available_port(settings.port, settings.host)
            logger.info(f"Using alternative port: {available_port}")
        else:
            available_port = settings.port

        # Log startup information
        logger.info(f"🌐 Server starting on {settings.host}:{available_port}")
        logger.info(f"📋 Base URL: http://{settings.host}:{available_port}")
        logger.info(f"📚 API Docs: http://{settings.host}:{available_port}/docs")
        logger.info(f"❤️ Health Check: http://{settings.host}:{available_port}/health")

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
