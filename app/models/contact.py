"""
Contact and person-related database models.
"""

from sqlalchemy import (
    Column, String, Boolean, ForeignKey, Date, Text, Integer, 
    Numeric, DateTime
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from app.models.base import Base, UUIDMixin, TimestampMixin


class Contact(Base, UUIDMixin, TimestampMixin):
    """Contact/person information model."""
    
    __tablename__ = "contacts"
    
    external_id = Column(String(100), index=True)
    email = Column(String(255), index=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    full_name = Column(String(500), index=True)
    job_title = Column(String(255))
    company_id = Column(
        UUID(as_uuid=True),
        ForeignKey("companies.id"),
        nullable=True
    )
    phone = Column(String(50))
    linkedin_url = Column(String(500))
    verified_email = Column(Boolean, default=False)
    email_deliverable = Column(Boolean)
    confidence_score = Column(Numeric(3, 2), default=0.0)
    last_enriched_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    company = relationship("Company", back_populates="contacts")
    social_profiles = relationship(
        "ContactSocialProfile", back_populates="contact", 
        cascade="all, delete-orphan"
    )
    employment_history = relationship(
        "EmploymentHistory", back_populates="contact", 
        cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return f"<Contact(email='{self.email}', name='{self.full_name}')>"


class ContactSocialProfile(Base, UUIDMixin, TimestampMixin):
    """Social media profiles for contacts."""
    
    __tablename__ = "contact_social_profiles"
    
    contact_id = Column(
        UUID(as_uuid=True),
        ForeignKey("contacts.id", ondelete="CASCADE"),
        nullable=False
    )
    platform = Column(String(50), nullable=False)
    url = Column(String(500), nullable=False)
    username = Column(String(100))
    followers_count = Column(Integer)
    verified = Column(Boolean, default=False)
    
    # Relationships
    contact = relationship("Contact", back_populates="social_profiles")
    
    def __repr__(self) -> str:
        return (f"<ContactSocialProfile(platform='{self.platform}', "
                f"username='{self.username}')>")


class EmploymentHistory(Base, UUIDMixin, TimestampMixin):
    """Employment history for contacts."""
    
    __tablename__ = "employment_history"
    
    contact_id = Column(
        UUID(as_uuid=True),
        ForeignKey("contacts.id", ondelete="CASCADE"),
        nullable=False
    )
    company_name = Column(String(500))
    job_title = Column(String(255))
    start_date = Column(Date)
    end_date = Column(Date)
    is_current = Column(Boolean, default=False)
    description = Column(Text)
    
    # Relationships
    contact = relationship("Contact", back_populates="employment_history")
    
    def __repr__(self) -> str:
        return (f"<EmploymentHistory(company='{self.company_name}', "
                f"title='{self.job_title}')>") 