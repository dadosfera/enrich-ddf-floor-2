"""Enhanced FastAPI application for Enrich DDF Floor 2.

Provides database integration and dynamic port configuration.
"""

import logging
import socket
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Any, Dict

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
        f"No available port found in range {start_port}-{start_port + max_attempts - 1!r}"
    )


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Application lifespan manager."""
    # Startup
    print(f"🚀 Starting {settings.app_name} v{settings.app_version!r}")
    print(f"📊 Database: {settings.database_url!r}")
    print(f"🔒 Debug mode: {settings.debug!r}")

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
        "message": f"Welcome to {settings.app_name!r}",
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


@app.get("/api/v1/companies", response_model=Dict[str, Any])
async def list_companies(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """List companies from database."""
    logger.info(f"📋 Fetching companies with skip={skip}, limit={limit!r}")
    try:
        companies = db.query(Company).offset(skip).limit(limit).all()
        company_list = [company.to_dict() for company in companies]
        total_count = db.query(Company).count()

        response = {
            "data": company_list,
            "total": total_count,
            "page": (skip // limit) + 1 if limit > 0 else 1,
            "size": limit,
            "success": True,
        }

        logger.info(f"✅ Successfully fetched {len(company_list)} companies")
        return response
    except Exception as e:
        logger.exception("❌ Failed to fetch companies")
        raise HTTPException(
            status_code=500, detail=f"Failed to fetch companies: {e!s!r}"
        ) from e


@app.post("/api/v1/companies", response_model=Dict[str, Any])
async def create_company(company_data: Dict[str, Any], db: Session = Depends(get_db)):
    """Create a new company."""
    logger.info(f"🏢 Creating new company: {company_data.get('name', 'Unknown')!r}")
    try:
        company = Company(**company_data)
        db.add(company)
        db.commit()
        db.refresh(company)

        response = {
            "success": True,
            "status": "created",
            "data": company.to_dict(),
            "message": f"Company '{company.name}' created successfully",
        }

        logger.info(f"✅ Successfully created company with ID: {company.id!r}")
        return response
    except Exception as e:
        db.rollback()
        logger.exception(f"❌ Failed to create company: {company_data!r}")
        raise HTTPException(
            status_code=400, detail=f"Failed to create company: {e!s!r}"
        ) from e


@app.get("/api/v1/contacts", response_model=Dict[str, Any])
async def list_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List contacts from database."""
    logger.info(f"👥 Fetching contacts with skip={skip}, limit={limit!r}")
    try:
        contacts = db.query(Contact).offset(skip).limit(limit).all()
        contact_list = [contact.to_dict() for contact in contacts]
        total_count = db.query(Contact).count()

        response = {
            "data": contact_list,
            "total": total_count,
            "page": (skip // limit) + 1 if limit > 0 else 1,
            "size": limit,
            "success": True,
        }

        logger.info(f"✅ Successfully fetched {len(contact_list)} contacts")
        return response
    except Exception as e:
        logger.exception("❌ Failed to fetch contacts")
        raise HTTPException(
            status_code=500, detail=f"Failed to fetch contacts: {e!s!r}"
        ) from e


@app.post("/api/v1/contacts", response_model=Dict[str, Any])
async def create_contact(contact_data: Dict[str, Any], db: Session = Depends(get_db)):
    """Create a new contact."""
    logger.info(f"👤 Creating new contact: {contact_data.get('name', 'Unknown')!r}")
    try:
        contact = Contact(**contact_data)
        db.add(contact)
        db.commit()
        db.refresh(contact)

        response = {
            "success": True,
            "status": "created",
            "data": contact.to_dict(),
            "message": f"Contact '{contact.name}' created successfully",
        }

        logger.info(f"✅ Successfully created contact with ID: {contact.id!r}")
        return response
    except Exception as e:
        db.rollback()
        logger.exception(f"❌ Failed to create contact: {contact_data!r}")
        raise HTTPException(
            status_code=400, detail=f"Failed to create contact: {e!s!r}"
        ) from e


@app.get("/api/v1/products", response_model=Dict[str, Any])
async def list_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List products from database."""
    logger.info(f"🛍️ Fetching products with skip={skip}, limit={limit!r}")
    try:
        products = db.query(Product).offset(skip).limit(limit).all()
        product_list = [product.to_dict() for product in products]
        total_count = db.query(Product).count()

        response = {
            "data": product_list,
            "total": total_count,
            "page": (skip // limit) + 1 if limit > 0 else 1,
            "size": limit,
            "success": True,
        }

        logger.info(f"✅ Successfully fetched {len(product_list)} products")
        return response
    except Exception as e:
        logger.exception("❌ Failed to fetch products")
        raise HTTPException(
            status_code=500, detail=f"Failed to fetch products: {e!s!r}"
        ) from e


@app.post("/api/v1/products", response_model=Dict[str, Any])
async def create_product(product_data: Dict[str, Any], db: Session = Depends(get_db)):
    """Create a new product."""
    logger.info(f"📦 Creating new product: {product_data.get('name', 'Unknown')!r}")
    try:
        product = Product(**product_data)
        db.add(product)
        db.commit()
        db.refresh(product)

        response = {
            "success": True,
            "status": "created",
            "data": product.to_dict(),
            "message": f"Product '{product.name}' created successfully",
        }

        logger.info(f"✅ Successfully created product with ID: {product.id!r}")
        return response
    except Exception as e:
        db.rollback()
        logger.exception(f"❌ Failed to create product: {product_data!r}")
        raise HTTPException(
            status_code=400, detail=f"Failed to create product: {e!s!r}"
        ) from e


# ==============================================================================
# ENRICHMENT ENDPOINTS
# ==============================================================================


@app.post("/api/v1/integrations/pdl/enrich-person")
async def enrich_person_pdl(request_data: Dict[str, Any]):
    """Enrich person data using People Data Labs API."""
    logger.info(f"🔍 PDL Person enrichment request: {request_data!r}")

    try:
        # Mock enrichment response for testing (replace with real PDL API call)
        enriched_data = {
            "success": True,
            "status": 200,
            "data": {
                "full_name": request_data.get("name", "Unknown Person"),
                "first_name": request_data.get("first_name", "Unknown"),
                "last_name": request_data.get("last_name", "Person"),
                "current_role": {
                    "title": "Software Engineer",
                    "company": "Tech Corp",
                    "seniority_level": "mid",
                },
                "experience": [
                    {
                        "company": "Tech Corp",
                        "title": "Software Engineer",
                        "start_date": "2020-01-01",
                    }
                ],
                "education": [
                    {
                        "school": "University of Technology",
                        "degree": "Bachelor of Computer Science",
                    }
                ],
                "emails": [request_data.get("email", "unknown@example.com")],
                "phone_numbers": ["+1-555-0123"],
                "linkedin_url": (
                    f"https://linkedin.com/in/"
                    f"{request_data.get('first_name', 'unknown').lower()}-"
                    f"{request_data.get('last_name', 'person').lower()!r}"
                ),
                "location": "San Francisco, CA",
                "skills": ["Python", "JavaScript", "FastAPI", "React"],
                "likelihood": 8,
            },
            "message": "Person enriched successfully (mock data)",
        }

        logger.info("✅ PDL Person enrichment successful (mock)")
        return enriched_data

    except Exception as e:
        logger.exception("❌ PDL Person enrichment failed")
        raise HTTPException(
            status_code=500, detail=f"Person enrichment failed: {str(e)!r}"
        ) from e


@app.post("/api/v1/integrations/pdl/enrich-company")
async def enrich_company_pdl(request_data: Dict[str, Any]):
    """Enrich company data using People Data Labs API."""
    logger.info(f"🏢 PDL Company enrichment request: {request_data!r}")

    try:
        # Mock enrichment response for testing (replace with real PDL API call)
        company_name = request_data.get("name", "Unknown Company")
        domain = request_data.get(
            "domain", f"{company_name.lower().replace(' ', '')}.com"
        )

        enriched_data = {
            "success": True,
            "status": 200,
            "data": {
                "name": company_name,
                "display_name": company_name,
                "size": "201-500",
                "employee_count": 350,
                "industry": "Technology",
                "sector": "Software",
                "website": f"https://{domain!r}",
                "domain": domain,
                "founded": 2010,
                "location": {
                    "city": "San Francisco",
                    "region": "California",
                    "country": "United States",
                },
                "linkedin_url": f"https://linkedin.com/company/{company_name.lower().replace(' ', '-')!r}",
                "twitter_url": f"https://twitter.com/{company_name.lower().replace(' ', '')!r}",
                "description": f"{company_name} is a leading technology company specializing in innovative software solutions.",
                "technologies": ["Python", "JavaScript", "AWS", "Docker"],
                "funding": {"total_funding": 50000000, "last_funding_type": "Series B"},
                "likelihood": 9,
            },
            "message": "Company enriched successfully (mock data)",
        }

        logger.info("✅ PDL Company enrichment successful (mock)")
        return enriched_data

    except Exception as e:
        logger.exception("❌ PDL Company enrichment failed")
        raise HTTPException(
            status_code=500, detail=f"Company enrichment failed: {str(e)!r}"
        ) from e


@app.post("/api/v1/integrations/wiza/enrich-profile")
async def enrich_linkedin_profile_wiza(request_data: Dict[str, Any]):
    """Enrich LinkedIn profile using Wiza API."""
    logger.info(f"🔗 Wiza LinkedIn enrichment request: {request_data!r}")

    try:
        linkedin_url = request_data.get("linkedin_url", "")

        # Mock enrichment response for testing (replace with real Wiza API call)
        enriched_data = {
            "success": True,
            "status": 200,
            "data": {
                "linkedin_url": linkedin_url,
                "first_name": "John",
                "last_name": "Smith",
                "full_name": "John Smith",
                "headline": "Senior Software Engineer at Tech Corp",
                "current_position": {
                    "title": "Senior Software Engineer",
                    "company": "Tech Corp",
                    "company_url": "https://linkedin.com/company/tech-corp",
                },
                "location": "San Francisco Bay Area",
                "industry": "Technology",
                "email": "john.smith@techcorp.com",
                "phone": "+1-555-0123",
                "experience": [
                    {
                        "title": "Senior Software Engineer",
                        "company": "Tech Corp",
                        "duration": "2 yrs",
                    },
                    {
                        "title": "Software Engineer",
                        "company": "StartupCo",
                        "duration": "1 yr 6 mos",
                    },
                ],
                "education": [
                    {"school": "Stanford University", "degree": "BS Computer Science"}
                ],
                "skills": ["Python", "React", "AWS", "Machine Learning"],
                "connections": 500,
            },
            "message": "LinkedIn profile enriched successfully (mock data)",
        }

        logger.info("✅ Wiza LinkedIn enrichment successful (mock)")
        return enriched_data

    except Exception as e:
        logger.exception("❌ Wiza LinkedIn enrichment failed")
        raise HTTPException(
            status_code=500, detail=f"LinkedIn profile enrichment failed: {str(e)!r}"
        ) from e


@app.post("/api/v1/enrich/person")
async def enrich_person_data(
    request_data: Dict[str, Any], db: Session = Depends(get_db)
):
    """Main enrichment endpoint for person data."""
    logger.info(f"🔍 Person enrichment request: {request_data!r}")

    try:
        # Import and use the real data enrichment engine
        from core.enrichment.real_data_enrichment import real_enrichment_engine

        # Use real data enrichment with fallback to mock data
        enriched_data = await real_enrichment_engine.enrich_person_real(request_data)

        # Create enriched person response
        enriched_person = {
            "original_data": request_data,
            "enriched_data": enriched_data,
            "enrichment_score": enriched_data.get("enrichment_score", 0),
            "data_sources": enriched_data.get("data_sources", []),
            "enriched_at": datetime.utcnow().isoformat(),
        }

        # Optionally save to database or update existing contact
        email = enriched_data.get("email")
        if email:
            contact = db.query(Contact).filter(Contact.email == email).first()
            if contact:
                # Update existing contact with enriched data
                contact.enrichment_data = enriched_person["enriched_data"]
                db.commit()
                logger.info(
                    f"✅ Updated existing contact {contact.id} with enriched data"
                )

        return {
            "success": True,
            "data": enriched_person,
            "message": "Person enriched successfully",
        }

    except Exception as e:
        logger.exception("❌ Person enrichment failed")
        raise HTTPException(
            status_code=500, detail=f"Person enrichment failed: {str(e)!r}"
        ) from e


@app.post("/api/v1/enrich/company")
async def enrich_company_data(
    request_data: Dict[str, Any], db: Session = Depends(get_db)
):
    """Main enrichment endpoint for company data."""
    logger.info(f"🏢 Company enrichment request: {request_data!r}")

    try:
        # Import and use the real data enrichment engine
        from core.enrichment.real_data_enrichment import real_enrichment_engine

        # Use real data enrichment with fallback to mock data
        enriched_data = await real_enrichment_engine.enrich_company_real(request_data)

        # Create enriched company response
        enriched_company = {
            "original_data": request_data,
            "enriched_data": enriched_data,
            "enrichment_score": enriched_data.get("enrichment_score", 0),
            "data_sources": enriched_data.get("data_sources", []),
            "enriched_at": datetime.utcnow().isoformat(),
        }

        # Optionally save to database or update existing company
        domain = enriched_data.get("domain")
        if domain:
            company = db.query(Company).filter(Company.domain == domain).first()
            if company:
                # Update existing company with enriched data
                company.enrichment_data = enriched_company["enriched_data"]
                db.commit()
                logger.info(
                    f"✅ Updated existing company {company.id} with enriched data"
                )

        return {
            "success": True,
            "data": enriched_company,
            "message": "Company enriched successfully",
        }

    except Exception as e:
        logger.exception("❌ Company enrichment failed")
        raise HTTPException(
            status_code=500, detail=f"Company enrichment failed: {str(e)!r}"
        ) from e


if __name__ == "__main__":
    # Find available port if configured port is occupied
    try:
        if not is_port_available(settings.port, settings.host):
            logger.warning(f"Port {settings.port} is occupied, finding alternative...")
            available_port = find_available_port(settings.port, settings.host)
            logger.info(f"Using alternative port: {available_port!r}")
        else:
            available_port = settings.port

        # Log startup information
        logger.info(f"🌐 Server starting on {settings.host}:{available_port!r}")
        logger.info(f"📋 Base URL: http://{settings.host}:{available_port!r}")
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
