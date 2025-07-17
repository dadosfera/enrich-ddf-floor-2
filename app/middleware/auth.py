"""
Authentication middleware for JWT and API key validation.
"""

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

import structlog

logger = structlog.get_logger(__name__)


class AuthMiddleware(BaseHTTPMiddleware):
    """Middleware for authentication and authorization."""
    
    async def dispatch(self, request: Request, call_next) -> Response:
        """Process request with authentication."""
        
        # Skip authentication for health check and docs
        skip_paths = ["/health", "/", "/docs", "/redoc", "/openapi.json"]
        if request.url.path in skip_paths:
            return await call_next(request)
        
        # TODO: Implement JWT and API key validation
        logger.debug("Processing authentication", path=request.url.path)
        
        response = await call_next(request)
        return response 