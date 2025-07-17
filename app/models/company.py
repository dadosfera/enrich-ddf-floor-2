"""
Company-related database models.
"""

from sqlalchemy import (
    Column, String, Text, Integer, Numeric, DateTime,
    Boolean, ForeignKey, UniqueConstraint
)
from sqlalchemy.orm import relationship

from app.models.base import Base, UUIDMixin, TimestampMixin


class Company(Base, UUIDMixin, TimestampMixin):
    """Core company information model."""
    
    __tablename__ = "companies"
    
    external_id = Column(String(100), index=True)
    country_code = Column(String(3), nullable=False, index=True)
    tax_id = Column(String(50), index=True)
    name = Column(String(500), nullable=False, index=True)
    legal_name = Column(String(500))
    status = Column(String(20), default="active", nullable=False)
    industry_code = Column(String(20))
    industry_description = Column(Text)
    company_size = Column(String(20))
    founded_year = Column(Integer)
    website = Column(String(255))
    phone = Column(String(50))
    email = Column(String(255))
    description = Column(Text)
    confidence_score = Column(Numeric(3, 2), default=0.0)
    last_enriched_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    addresses = relationship(
        "CompanyAddress", back_populates="company", 
        cascade="all, delete-orphan"
    )
    financials = relationship(
        "CompanyFinancials", back_populates="company", 
        cascade="all, delete-orphan"
    )
    contacts = relationship(
        "Contact", back_populates="company"
    )
    
    def __repr__(self) -> str:
        return f"<Company(name='{self.name}', country='{self.country_code}')>"


class CompanyAddress(Base, UUIDMixin, TimestampMixin):
    """Company address information model."""
    
    __tablename__ = "company_addresses"
    
    company_id = Column(
        ForeignKey("companies.id", ondelete="CASCADE"),
        nullable=False
    )
    address_type = Column(String(20), default="headquarters", nullable=False)
    street_address = Column(Text)
    city = Column(String(255))
    state = Column(String(255))
    postal_code = Column(String(20))
    country_code = Column(String(3))
    latitude = Column(Numeric(10, 8))
    longitude = Column(Numeric(11, 8))
    is_primary = Column(Boolean, default=False)
    
    # Relationships
    company = relationship("Company", back_populates="addresses")
    
    def __repr__(self) -> str:
        return (f"<CompanyAddress(type='{self.address_type}', "
                f"city='{self.city}')>")


class CompanyFinancials(Base, UUIDMixin, TimestampMixin):
    """Company financial information model."""
    
    __tablename__ = "company_financials"
    
    company_id = Column(
        ForeignKey("companies.id", ondelete="CASCADE"),
        nullable=False
    )
    year = Column(Integer, nullable=False)
    revenue = Column(Numeric(15, 2))
    currency = Column(String(3))
    employees_count = Column(Integer)
    credit_rating = Column(String(10))
    risk_score = Column(Numeric(3, 2))
    source = Column(String(100))
    
    # Relationships
    company = relationship("Company", back_populates="financials")
    
    # Constraints
    __table_args__ = (
        UniqueConstraint('company_id', 'year', name='_company_year_uc'),
    )
    
    def __repr__(self) -> str:
        return (f"<CompanyFinancials(company_id='{self.company_id}', "
                f"year={self.year})>") 