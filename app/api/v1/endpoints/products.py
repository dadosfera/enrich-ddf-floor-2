"""
Product classification endpoints.
"""

from fastapi import APIRouter

router = APIRouter()


@router.post("/classify")
async def classify_product():
    """Classify product with NCM/CNAE codes."""
    return {
        "message": "Product classification - TODO: Implement classification"
    }


@router.get("/ncm/{ncm_code}")
async def get_ncm_info(ncm_code: str):
    """Get NCM code information."""
    return {
        "ncm_code": ncm_code,
        "message": "NCM info - TODO: Implement NCM lookup"
    }


@router.get("/cnae/{cnae_code}")
async def get_cnae_info(cnae_code: str):
    """Get CNAE code information."""
    return {
        "cnae_code": cnae_code,
        "message": "CNAE info - TODO: Implement CNAE lookup"
    }