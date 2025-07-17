"""
Structured logging configuration using structlog.
"""

import logging
import sys
from typing import Any

import structlog

from app.core.config import settings


def setup_logging() -> None:
    """Configure structured logging for the application."""
    
    # Configure standard library logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, settings.LOG_LEVEL.upper()),
    )
    
    # Configure structlog
    processors = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
    ]
    
    if settings.LOG_FORMAT == "json":
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer())
    
    structlog.configure(
        processors=processors,
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str) -> structlog.BoundLogger:
    """Get a logger instance with the given name."""
    return structlog.get_logger(name)


def log_request(
    method: str,
    path: str,
    status_code: int,
    response_time: float,
    **kwargs: Any
) -> None:
    """Log HTTP request information."""
    logger = get_logger("request")
    logger.info(
        "HTTP request",
        method=method,
        path=path,
        status_code=status_code,
        response_time_ms=round(response_time * 1000, 2),
        **kwargs
    )


def log_external_api_call(
    service: str,
    endpoint: str,
    method: str,
    status_code: int,
    response_time: float,
    **kwargs: Any
) -> None:
    """Log external API call information."""
    logger = get_logger("external_api")
    logger.info(
        "External API call",
        service=service,
        endpoint=endpoint,
        method=method,
        status_code=status_code,
        response_time_ms=round(response_time * 1000, 2),
        **kwargs
    )


def log_enrichment_operation(
    operation: str,
    entity_type: str,
    entity_id: str,
    data_sources: list,
    confidence_score: float,
    **kwargs: Any
) -> None:
    """Log data enrichment operation."""
    logger = get_logger("enrichment")
    logger.info(
        "Enrichment operation",
        operation=operation,
        entity_type=entity_type,
        entity_id=entity_id,
        data_sources=data_sources,
        confidence_score=confidence_score,
        **kwargs
    ) 