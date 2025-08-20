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
            status_code=500, detail=f"Failed to fetch companies: {e!r}"
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
            status_code=400, detail=f"Failed to create company: {e!r}"
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
            status_code=500, detail=f"Failed to fetch contacts: {e!r}"
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
            status_code=400, detail=f"Failed to create contact: {e!r}"
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
            status_code=500, detail=f"Failed to fetch products: {e!r}"
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
            status_code=400, detail=f"Failed to create product: {e!r}"
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
        api_key = request_data.get("api_key")
        if not api_key:
            raise HTTPException(status_code=400, detail="API key is required")

        linkedin_url = request_data.get("linkedin_url")
        if not linkedin_url:
            raise HTTPException(status_code=400, detail="LinkedIn URL is required")

        include_emails = request_data.get("include_emails", True)
        include_phone = request_data.get("include_phone", True)

        # Import Wiza service
        from services.third_party.wiza import WizaService

        wiza_service = WizaService(api_key=api_key)

        # Enrich LinkedIn profile
        result = await wiza_service.enrich_linkedin_profile(
            linkedin_url, include_emails, include_phone
        )

        if result.get("success"):
            logger.info("✅ Wiza LinkedIn enrichment successful")
            return {
                "success": True,
                "data": result["profile"],
                "credits_used": result.get("credits_used", 0),
                "credits_remaining": result.get("credits_remaining", 0),
                "message": result.get(
                    "message", "LinkedIn profile enriched successfully"
                ),
            }
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Wiza LinkedIn enrichment failed: {result.get('error')}",
            )

    except Exception as e:
        logger.exception("❌ Wiza LinkedIn enrichment failed")
        raise HTTPException(
            status_code=500, detail=f"LinkedIn profile enrichment failed: {str(e)!r}"
        ) from e


@app.post("/api/v1/integrations/wiza/find-email")
async def find_email_wiza(request_data: Dict[str, Any]):
    """Find email using Wiza API."""
    logger.info(f"📧 Wiza email finding request: {request_data!r}")

    try:
        api_key = request_data.get("api_key")
        if not api_key:
            raise HTTPException(status_code=400, detail="API key is required")

        first_name = request_data.get("first_name")
        last_name = request_data.get("last_name")
        company_domain = request_data.get("company_domain")

        if not all([first_name, last_name, company_domain]):
            raise HTTPException(
                status_code=400,
                detail="First name, last name, and company domain are required",
            )

        linkedin_url = request_data.get("linkedin_url")

        # Import Wiza service
        from services.third_party.wiza import WizaService

        wiza_service = WizaService(api_key=api_key)

        # Find email
        result = await wiza_service.find_email(
            str(first_name), str(last_name), str(company_domain), linkedin_url
        )

        if result.get("success"):
            logger.info("✅ Wiza email finding successful")
            return {
                "success": True,
                "data": result["emails"],
                "credits_used": result.get("credits_used", 0),
                "credits_remaining": result.get("credits_remaining", 0),
                "message": result.get("message", "Email finding completed"),
            }
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Wiza email finding failed: {result.get('error')}",
            )

    except Exception as e:
        logger.exception("❌ Wiza email finding failed")
        raise HTTPException(
            status_code=500, detail=f"Email finding failed: {str(e)!r}"
        ) from e


@app.post("/api/v1/integrations/wiza/enrich-company")
async def enrich_company_wiza(request_data: Dict[str, Any]):
    """Enrich company using Wiza API."""
    logger.info(f"🏢 Wiza company enrichment request: {request_data!r}")

    try:
        api_key = request_data.get("api_key")
        if not api_key:
            raise HTTPException(status_code=400, detail="API key is required")

        company_domain = request_data.get("company_domain")
        company_name = request_data.get("company_name")
        linkedin_url = request_data.get("linkedin_url")

        if not any([company_domain, company_name, linkedin_url]):
            raise HTTPException(
                status_code=400, detail="At least one company identifier is required"
            )

        # Import Wiza service
        from services.third_party.wiza import WizaService

        wiza_service = WizaService(api_key=api_key)

        # Enrich company
        result = await wiza_service.enrich_company(
            company_domain, company_name, linkedin_url
        )

        if result.get("success"):
            logger.info("✅ Wiza company enrichment successful")
            return {
                "success": True,
                "data": result["company"],
                "credits_used": result.get("credits_used", 0),
                "credits_remaining": result.get("credits_remaining", 0),
                "message": result.get("message", "Company enrichment completed"),
            }
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Wiza company enrichment failed: {result.get('error')}",
            )

    except Exception as e:
        logger.exception("❌ Wiza company enrichment failed")
        raise HTTPException(
            status_code=500, detail=f"Company enrichment failed: {str(e)!r}"
        ) from e


@app.get("/api/v1/integrations/wiza/credits")
async def get_wiza_credits(api_key: str):
    """Get Wiza API credits information."""
    logger.info("📊 Wiza credits check request")

    try:
        # Import Wiza service
        from services.third_party.wiza import WizaService

        wiza_service = WizaService(api_key=api_key)

        # Get credits
        result = await wiza_service.get_credits()

        if result.get("success"):
            logger.info("✅ Wiza credits check successful")
            return {
                "success": True,
                "data": {"credits": result["credits"]},
                "message": result.get("message", "Credits retrieved successfully"),
            }
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Wiza credits check failed: {result.get('error')}",
            )

    except Exception as e:
        logger.exception("❌ Wiza credits check failed")
        raise HTTPException(
            status_code=500, detail=f"Wiza credits check failed: {str(e)!r}"
        ) from e


@app.post("/api/v1/integrations/github/enrich-profile")
async def enrich_github_profile(request_data: Dict[str, Any]):
    """Enrich GitHub profile data."""
    logger.info(f"🐙 GitHub profile enrichment request: {request_data!r}")

    try:
        username = request_data.get("username")
        if not username:
            raise HTTPException(status_code=400, detail="Username is required")

        # Import GitHub service
        from services.third_party.github import GitHubService

        github_service = GitHubService()

        # Enrich profile
        result = github_service.enrich_developer_profile(username)

        if result.get("success"):
            logger.info("✅ GitHub profile enrichment successful")
            return {
                "success": True,
                "data": result,
                "message": "GitHub profile enriched successfully",
            }
        else:
            raise HTTPException(
                status_code=404,
                detail=f"GitHub profile not found or error: {result.get('error')}",
            )

    except Exception as e:
        logger.exception("❌ GitHub profile enrichment failed")
        raise HTTPException(
            status_code=500, detail=f"GitHub profile enrichment failed: {str(e)!r}"
        ) from e


@app.post("/api/v1/integrations/github/enrich-organization")
async def enrich_github_organization(request_data: Dict[str, Any]):
    """Enrich GitHub organization data."""
    logger.info(f"🏢 GitHub organization enrichment request: {request_data!r}")

    try:
        org_name = request_data.get("organization") or request_data.get("org_name")
        if not org_name:
            raise HTTPException(status_code=400, detail="Organization name is required")

        # Import GitHub service
        from services.third_party.github import GitHubService

        github_service = GitHubService()

        # Enrich organization
        result = github_service.enrich_organization(org_name)

        if result.get("success"):
            logger.info("✅ GitHub organization enrichment successful")
            return {
                "success": True,
                "data": result,
                "message": "GitHub organization enriched successfully",
            }
        else:
            raise HTTPException(
                status_code=404,
                detail=f"GitHub organization not found or error: {result.get('error')}",
            )

    except Exception as e:
        logger.exception("❌ GitHub organization enrichment failed")
        raise HTTPException(
            status_code=500, detail=f"GitHub organization enrichment failed: {str(e)!r}"
        ) from e


@app.get("/api/v1/integrations/github/rate-limit")
async def get_github_rate_limit():
    """Get GitHub API rate limit information."""
    logger.info("📊 GitHub rate limit check request")

    try:
        # Import GitHub service
        from services.third_party.github import GitHubService

        github_service = GitHubService()

        # Get rate limit info
        result = github_service.get_rate_limit_info()

        if "error" not in result:
            logger.info("✅ GitHub rate limit check successful")
            return {
                "success": True,
                "data": result,
                "message": "GitHub rate limit retrieved successfully",
            }
        else:
            raise HTTPException(
                status_code=500,
                detail=f"GitHub rate limit check failed: {result.get('error')}",
            )

    except Exception as e:
        logger.exception("❌ GitHub rate limit check failed")
        raise HTTPException(
            status_code=500, detail=f"GitHub rate limit check failed: {str(e)!r}"
        ) from e


@app.post("/api/v1/integrations/surfe/search-people")
async def search_people_surfe(request_data: Dict[str, Any]):
    """Search for people using Surfe API."""
    logger.info(f"🔍 Surfe people search request: {request_data!r}")

    try:
        api_key = request_data.get("api_key")
        if not api_key:
            raise HTTPException(status_code=400, detail="API key is required")

        filters = request_data.get("filters", {})
        limit = request_data.get("limit", 10)
        offset = request_data.get("offset", 0)

        # Import Surfe service
        from services.third_party.surfe import SurfeService

        surfe_service = SurfeService(api_key=api_key)

        # Search people
        result = await surfe_service.search_people(filters, limit, offset)

        if result.get("success"):
            logger.info("✅ Surfe people search successful")
            return {
                "success": True,
                "data": result["people"],
                "total_count": result.get("total_count", 0),
                "message": result.get("message", "People search completed"),
            }
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Surfe people search failed: {result.get('error')}",
            )

    except Exception as e:
        logger.exception("❌ Surfe people search failed")
        raise HTTPException(
            status_code=500, detail=f"Surfe people search failed: {str(e)!r}"
        ) from e


@app.post("/api/v1/integrations/surfe/enrich-people")
async def enrich_people_surfe(request_data: Dict[str, Any]):
    """Enrich people data using Surfe API."""
    logger.info(f"🔍 Surfe people enrichment request: {request_data!r}")

    try:
        api_key = request_data.get("api_key")
        if not api_key:
            raise HTTPException(status_code=400, detail="API key is required")

        people = request_data.get("people", [])
        if not people:
            raise HTTPException(status_code=400, detail="People data is required")

        include_email = request_data.get("include_email", True)
        include_mobile = request_data.get("include_mobile", False)

        # Import Surfe service
        from services.third_party.surfe import SurfeService

        surfe_service = SurfeService(api_key=api_key)

        # Enrich people
        result = await surfe_service.enrich_people(
            people, include_email, include_mobile
        )

        if result.get("success"):
            logger.info("✅ Surfe people enrichment successful")
            return {
                "success": True,
                "data": result["people"],
                "credits_used": result.get("credits_used", {}),
                "credits_remaining": result.get("credits_remaining", {}),
                "message": result.get("message", "People enrichment completed"),
            }
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Surfe people enrichment failed: {result.get('error')}",
            )

    except Exception as e:
        logger.exception("❌ Surfe people enrichment failed")
        raise HTTPException(
            status_code=500, detail=f"Surfe people enrichment failed: {str(e)!r}"
        ) from e


@app.post("/api/v1/integrations/surfe/search-companies")
async def search_companies_surfe(request_data: Dict[str, Any]):
    """Search for companies using Surfe API."""
    logger.info(f"🏢 Surfe company search request: {request_data!r}")

    try:
        api_key = request_data.get("api_key")
        if not api_key:
            raise HTTPException(status_code=400, detail="API key is required")

        filters = request_data.get("filters", {})
        limit = request_data.get("limit", 10)
        offset = request_data.get("offset", 0)

        # Import Surfe service
        from services.third_party.surfe import SurfeService

        surfe_service = SurfeService(api_key=api_key)

        # Search companies
        result = await surfe_service.search_companies(filters, limit, offset)

        if result.get("success"):
            logger.info("✅ Surfe company search successful")
            return {
                "success": True,
                "data": result["companies"],
                "total_count": result.get("total_count", 0),
                "message": result.get("message", "Company search completed"),
            }
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Surfe company search failed: {result.get('error')}",
            )

    except Exception as e:
        logger.exception("❌ Surfe company search failed")
        raise HTTPException(
            status_code=500, detail=f"Surfe company search failed: {str(e)!r}"
        ) from e


@app.post("/api/v1/integrations/surfe/enrich-companies")
async def enrich_companies_surfe(request_data: Dict[str, Any]):
    """Enrich company data using Surfe API."""
    logger.info(f"🏢 Surfe company enrichment request: {request_data!r}")

    try:
        api_key = request_data.get("api_key")
        if not api_key:
            raise HTTPException(status_code=400, detail="API key is required")

        companies = request_data.get("companies", [])
        if not companies:
            raise HTTPException(status_code=400, detail="Companies data is required")

        # Import Surfe service
        from services.third_party.surfe import SurfeService

        surfe_service = SurfeService(api_key=api_key)

        # Enrich companies
        result = await surfe_service.enrich_companies(companies)

        if result.get("success"):
            logger.info("✅ Surfe company enrichment successful")
            return {
                "success": True,
                "data": result["companies"],
                "message": result.get("message", "Company enrichment completed"),
            }
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Surfe company enrichment failed: {result.get('error')}",
            )

    except Exception as e:
        logger.exception("❌ Surfe company enrichment failed")
        raise HTTPException(
            status_code=500, detail=f"Surfe company enrichment failed: {str(e)!r}"
        ) from e


@app.get("/api/v1/integrations/surfe/credits")
async def get_surfe_credits(api_key: str):
    """Get Surfe API credits information."""
    logger.info("📊 Surfe credits check request")

    try:
        # Import Surfe service
        from services.third_party.surfe import SurfeService

        surfe_service = SurfeService(api_key=api_key)

        # Get credits
        result = await surfe_service.get_credits()

        if result.get("success"):
            logger.info("✅ Surfe credits check successful")
            return {
                "success": True,
                "data": result["credits"],
                "message": result.get("message", "Credits retrieved successfully"),
            }
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Surfe credits check failed: {result.get('error')}",
            )

    except Exception as e:
        logger.exception("❌ Surfe credits check failed")
        raise HTTPException(
            status_code=500, detail=f"Surfe credits check failed: {str(e)!r}"
        ) from e


@app.post("/api/v1/enrich/person")
async def enrich_person_data(
    request_data: Dict[str, Any], db: Session = Depends(get_db)
):
    """Main enrichment endpoint for person data."""  # TODO: Review loop variable naming (PLW2901)  # TODO: Review loop variable naming (PLW2901)
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
    """Main enrichment endpoint for company data."""  # TODO: Review loop variable naming (PLW2901)  # TODO: Review loop variable naming (PLW2901)
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
