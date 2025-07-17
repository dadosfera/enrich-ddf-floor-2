"""
Enrichment history and data source tracking models.
"""

from sqlalchemy import (
    Column, String, Text, Integer, DateTime, Numeric, 
    Boolean, ForeignKey
)
from sqlalchemy.dialects.postgresql import JSONB, ARRAY, UUID

from app.models.base import Base, UUIDMixin, TimestampMixin


class EnrichmentHistory(Base, UUIDMixin, TimestampMixin):
    """Track enrichment operations and their results."""
    
    __tablename__ = "enrichment_history"
    
    entity_type = Column(String(50), nullable=False, index=True)
    entity_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    operation = Column(String(50), nullable=False)
    data_sources = Column(ARRAY(Text), default=[])
    input_data = Column(JSONB)
    output_data = Column(JSONB)
    confidence_score = Column(Numeric(3, 2))
    processing_time_ms = Column(Integer)
    status = Column(String(20), default="completed", nullable=False)
    error_message = Column(Text)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True
    )
    
    def __repr__(self) -> str:
        return (f"<EnrichmentHistory(entity_type='{self.entity_type}', "
                f"operation='{self.operation}')>")


class DataSource(Base, UUIDMixin, TimestampMixin):
    """Data source configuration and statistics."""
    
    __tablename__ = "data_sources"
    
    name = Column(String(100), nullable=False, unique=True, index=True)
    display_name = Column(String(200))
    description = Column(Text)
    base_url = Column(String(500))
    country_codes = Column(ARRAY(String), default=[])
    supported_entities = Column(ARRAY(String), default=[])
    rate_limit_per_minute = Column(Integer, default=60)
    rate_limit_per_day = Column(Integer)
    cost_per_request = Column(Numeric(10, 4))
    is_active = Column(Boolean, default=True)
    requires_authentication = Column(Boolean, default=True)
    api_version = Column(String(20))
    
    # Statistics
    total_requests = Column(Integer, default=0)
    successful_requests = Column(Integer, default=0)
    failed_requests = Column(Integer, default=0)
    average_response_time_ms = Column(Integer)
    last_successful_request_at = Column(DateTime(timezone=True))
    last_failed_request_at = Column(DateTime(timezone=True))
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate percentage."""
        if self.total_requests == 0:
            return 0.0
        return (self.successful_requests / self.total_requests) * 100
    
    def __repr__(self) -> str:
        return f"<DataSource(name='{self.name}', active={self.is_active})>" 