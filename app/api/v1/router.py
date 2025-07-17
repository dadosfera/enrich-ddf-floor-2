"""
Main API router for v1 endpoints.
"""

from fastapi import APIRouter

from app.api.v1.endpoints import companies, contacts, products, auth

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["authentication"]
)

api_router.include_router(
    companies.router,
    prefix="/companies",
    tags=["companies"]
)

api_router.include_router(
    contacts.router,
    prefix="/contacts", 
    tags=["contacts"]
)

api_router.include_router(
    products.router,
    prefix="/products",
    tags=["products"]
) 