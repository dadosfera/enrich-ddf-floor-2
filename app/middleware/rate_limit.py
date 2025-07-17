"""
Rate limiting middleware using Redis.
"""

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

import structlog

logger = structlog.get_logger(__name__)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Middleware for rate limiting API requests."""
    
    async def dispatch(self, request: Request, call_next) -> Response:
        """Process request with rate limiting."""
        
        # Skip rate limiting for health check
        if request.url.path in ["/health", "/"]:
            return await call_next(request)
        
        # TODO: Implement Redis-based rate limiting
        logger.debug("Processing rate limit", path=request.url.path)
        
        response = await call_next(request)
        return response 