"""Database models for Enrich DDF Floor 2."""

from datetime import datetime
from typing import Optional

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, Boolean, Float, JSON
from sqlalchemy.orm import relationship

from .connection import Base


class Company(Base):
    """Company model for storing company information."""
    
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    domain = Column(String(255), unique=True, index=True)
    industry = Column(String(100))
    size = Column(String(50))
    location = Column(String(255))
    description = Column(Text)
    website = Column(String(255))
    phone = Column(String(50))
    email = Column(String(255))
    enrichment_data = Column(JSON)
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    contacts = relationship("Contact", back_populates="company")


class Contact(Base):
    """Contact model for storing contact information."""
    
    __tablename__ = "contacts"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True)
    phone = Column(String(50))
    job_title = Column(String(255))
    department = Column(String(100))
    company_id = Column(Integer, ForeignKey("companies.id"))
    linkedin_url = Column(String(255))
    twitter_url = Column(String(255))
    enrichment_data = Column(JSON)
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    company = relationship("Company", back_populates="contacts")


class Product(Base):
    """Product model for storing product information."""
    
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    sku = Column(String(100), unique=True, index=True)
    category = Column(String(100))
    subcategory = Column(String(100))
    brand = Column(String(100))
    description = Column(Text)
    price = Column(Float)
    currency = Column(String(10), default="USD")
    weight = Column(Float)
    dimensions = Column(String(100))
    stock_quantity = Column(Integer, default=0)
    product_url = Column(String(255))
    image_url = Column(String(255))
    classification_data = Column(JSON)
    enrichment_data = Column(JSON)
    is_active = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
