"""Enhanced FastAPI application for Enrich DDF Floor 2 with database integration."""

from contextlib import asynccontextmanager
from datetime import datetime
from typing import Any, Dict, List

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from config import settings
from database.connection import create_tables, get_db
from database.models import Company, Contact, Product


# Create database tables on startup
create_tables()


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: ARG001
    """Application lifespan manager."""
    # Startup
    print(f"🚀 Starting {settings.app_name} v{settings.app_version}")
    print(f"📊 Database: {settings.database_url}")
    print(f"🔒 Debug mode: {settings.debug}")
    yield
    # Shutdown
    print("🛑 Shutting down application...")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Unified Data Enrichment Platform with Database Integration",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint with application information."""
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.app_version,
        "status": "running",
        "docs_url": "/docs",
        "timestamp": datetime.utcnow().isoformat(),
    }


@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """Enhanced health check with database connectivity."""
    try:
        # Test database connection
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {e!s}"

    return {
        "status": "healthy",
        "database": db_status,
        "timestamp": datetime.utcnow().isoformat(),
        "version": settings.app_version,
    }


# Company endpoints with database integration
@app.post("/api/v1/companies", response_model=Dict[str, Any])
async def create_company(company_data: Dict[str, Any], db: Session = Depends(get_db)):
    """Create a new company with database persistence."""
    try:
        company = Company(
            name=company_data.get("name", "Unknown Company"),
            domain=company_data.get("domain"),
            industry=company_data.get("industry"),
            size=company_data.get("size"),
            location=company_data.get("location"),
            description=company_data.get("description"),
            website=company_data.get("website"),
            phone=company_data.get("phone"),
            email=company_data.get("email"),
        )

        db.add(company)
        db.commit()
        db.refresh(company)

        return {
            "message": "Company created successfully",
            "data": company.to_dict(),
            "status": "created",
            "id": company.id,
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create company: {e!s}",
        ) from e


@app.get("/api/v1/companies", response_model=List[Dict[str, Any]])
async def list_companies(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """List companies from database."""
    companies = db.query(Company).offset(skip).limit(limit).all()
    return [company.to_dict() for company in companies]


# Contact endpoints with database integration
@app.post("/api/v1/contacts", response_model=Dict[str, Any])
async def create_contact(contact_data: Dict[str, Any], db: Session = Depends(get_db)):
    """Create a new contact with database persistence."""
    try:
        contact = Contact(
            first_name=contact_data.get("first_name", "Unknown"),
            last_name=contact_data.get("last_name", "Contact"),
            email=contact_data.get("email", "unknown@example.com"),
            phone=contact_data.get("phone"),
            job_title=contact_data.get("job_title"),
            department=contact_data.get("department"),
            linkedin_url=contact_data.get("linkedin_url"),
            twitter_url=contact_data.get("twitter_url"),
            company_id=contact_data.get("company_id"),
        )

        db.add(contact)
        db.commit()
        db.refresh(contact)

        return {
            "message": "Contact created successfully",
            "data": contact.to_dict(),
            "status": "created",
            "id": contact.id,
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create contact: {e!s}",
        ) from e


@app.get("/api/v1/contacts", response_model=List[Dict[str, Any]])
async def list_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List contacts from database."""
    contacts = db.query(Contact).offset(skip).limit(limit).all()
    return [contact.to_dict() for contact in contacts]


# Product endpoints with database integration
@app.post("/api/v1/products", response_model=Dict[str, Any])
async def create_product(product_data: Dict[str, Any], db: Session = Depends(get_db)):
    """Create a new product with database persistence."""
    try:
        product = Product(
            name=product_data.get("name", "Unknown Product"),
            sku=product_data.get("sku"),
            category=product_data.get("category"),
            subcategory=product_data.get("subcategory"),
            brand=product_data.get("brand"),
            description=product_data.get("description"),
            price=product_data.get("price"),
            currency=product_data.get("currency", "USD"),
        )

        db.add(product)
        db.commit()
        db.refresh(product)

        return {
            "message": "Product created successfully",
            "data": product.to_dict(),
            "status": "created",
            "id": product.id,
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create product: {e!s}",
        ) from e


@app.get("/api/v1/products", response_model=List[Dict[str, Any]])
async def list_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List products from database."""
    products = db.query(Product).offset(skip).limit(limit).all()
    return [product.to_dict() for product in products]


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )
