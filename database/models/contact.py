"""Contact database model."""

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import relationship

from database.models.base import BaseModel


class Contact(BaseModel):
    """Contact model for storing contact information."""

    # Basic contact information
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone = Column(String(50))
    job_title = Column(String(255))
    department = Column(String(100))

    # Company relationship
    company_id = Column(Integer, ForeignKey("companys.id"), nullable=True)
    company = relationship("Company", backref="contacts")

    # Social and professional links
    linkedin_url = Column(String(500))
    twitter_url = Column(String(500))

    # Enrichment data (JSON for flexibility)
    enrichment_data = Column(JSON, default=dict)

    # Status flags
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    @property
    def full_name(self):
        """Get full name of contact."""
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        """String representation of Contact."""
        return f"<Contact(id={self.id}, name='{self.full_name}', email='{self.email}')>"
