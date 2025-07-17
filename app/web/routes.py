"""
Web interface routes for serving HTML templates.
"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os

router = APIRouter()

# Set up templates
template_dir = os.path.join(os.path.dirname(__file__), "..", "templates")
templates = Jinja2Templates(directory=template_dir)


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve the main homepage."""
    context = {
        "request": request,
        "product_count": "10,000+",
        "section_count": "21",
        "chapter_count": "97",
        "sections": [
            {"code": "I", "description": "Live animals; animal products", 
             "chapter_count": 5},
            {"code": "II", "description": "Vegetable products", 
             "chapter_count": 5},
            {"code": "III", "description": "Animal or vegetable fats and oils", 
             "chapter_count": 1},
            {"code": "IV", "description": "Prepared foodstuffs; beverages", 
             "chapter_count": 6},
            {"code": "V", "description": "Mineral products", 
             "chapter_count": 3},
            {"code": "VI", "description": "Products of the chemical industries", 
             "chapter_count": 6},
        ]
    }
    return templates.TemplateResponse("index_fastapi.html", context)


@router.get("/search", response_class=HTMLResponse)
async def search(request: Request, q: str = ""):
    """Serve the search page."""
    context = {
        "request": request,
        "query": q,
        "results": [],  # TODO: Implement search functionality
    }
    return templates.TemplateResponse("search_fastapi.html", context)


@router.get("/browse", response_class=HTMLResponse)
async def browse(request: Request):
    """Serve the browse page."""
    context = {
        "request": request,
        "sections": [
            {"code": "I", "description": "Live animals; animal products", 
             "chapter_count": 5},
            {"code": "II", "description": "Vegetable products", 
             "chapter_count": 5},
            {"code": "III", "description": "Animal or vegetable fats and oils", 
             "chapter_count": 1},
        ]
    }
    return templates.TemplateResponse("browse.html", context)


@router.get("/translation", response_class=HTMLResponse)
async def translation(request: Request):
    """Serve the translation page."""
    context = {"request": request}
    return templates.TemplateResponse("translation.html", context)


@router.get("/ai-translation", response_class=HTMLResponse)
async def ai_translation(request: Request):
    """Serve the AI translation page."""
    context = {"request": request}
    return templates.TemplateResponse("ai_translation.html", context)


@router.get("/import-data", response_class=HTMLResponse)
async def import_data_dashboard(request: Request):
    """Serve the import data dashboard."""
    context = {"request": request}
    return templates.TemplateResponse("import_data_dashboard.html", context)


@router.get("/web-scraper", response_class=HTMLResponse)
async def web_scraper(request: Request):
    """Serve the web scraper page."""
    context = {"request": request}
    return templates.TemplateResponse("web_scraper.html", context)


@router.get("/integrations", response_class=HTMLResponse)
async def integrations(request: Request):
    """Serve the integrations page."""
    context = {"request": request}
    return templates.TemplateResponse("integrations.html", context)


@router.get("/cache", response_class=HTMLResponse)
async def cache_stats(request: Request):
    """Serve the cache stats page."""
    context = {"request": request}
    return templates.TemplateResponse("cache_stats.html", context)


@router.get("/usage-billing", response_class=HTMLResponse)
async def usage_billing(request: Request):
    """Serve the usage and billing page."""
    context = {"request": request}
    return templates.TemplateResponse("usage_billing.html", context)


@router.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    """Serve the about page."""
    context = {"request": request}
    return templates.TemplateResponse("about.html", context)


@router.get("/product/{product_id}", response_class=HTMLResponse)
async def product_detail(request: Request, product_id: str):
    """Serve the product detail page."""
    context = {
        "request": request,
        "product": {
            "ncm_code": product_id,
            "description": "Sample Product Description",
            "category": "Sample Category"
        }
    }
    return templates.TemplateResponse("product_detail.html", context) 