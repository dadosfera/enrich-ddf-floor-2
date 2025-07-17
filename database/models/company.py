"""Company database model."""

from sqlalchemy import Boolean, Column, String, Text
from sqlalchemy.dialects.postgresql import JSON

from database.models.base import BaseModel


class Company(BaseModel):
    """Company model for storing company information."""

    name = Column(String(255), nullable=False, index=True)
    domain = Column(String(255), unique=True, index=True)
    industry = Column(String(100))
    size = Column(String(50))  # e.g., "1-10", "11-50", "51-200"
    location = Column(String(255))
    description = Column(Text)
    website = Column(String(500))
    phone = Column(String(50))
    email = Column(String(255))

    # Enrichment data (JSON for flexibility)
    enrichment_data = Column(JSON, default=dict)

    # Status flags
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    def __repr__(self):
        """String representation of Company."""
        return f"<Company(id={self.id}, name='{self.name}', domain='{self.domain}')>"
