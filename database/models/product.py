"""Product database model."""

from sqlalchemy import Boolean, Column, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import JSON

from database.models.base import BaseModel


class Product(BaseModel):
    """Product model for storing product information."""

    # Basic product information
    name = Column(String(255), nullable=False, index=True)
    sku = Column(String(100), unique=True, index=True)
    category = Column(String(100))
    subcategory = Column(String(100))
    brand = Column(String(100))
    description = Column(Text)

    # Pricing information
    price = Column(Numeric(10, 2))
    currency = Column(String(3), default="USD")

    # Product attributes
    weight = Column(Numeric(10, 2))
    dimensions = Column(String(100))  # e.g., "10x5x3 cm"
    color = Column(String(50))
    material = Column(String(100))

    # Inventory and status
    stock_quantity = Column(Integer, default=0)
    min_stock_level = Column(Integer, default=0)

    # URLs and references
    product_url = Column(String(500))
    image_url = Column(String(500))

    # Classification and enrichment data
    classification_data = Column(JSON, default=dict)
    enrichment_data = Column(JSON, default=dict)

    # Status flags
    is_active = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)

    def __repr__(self):
        """String representation of Product."""
        return f"<Product(id={self.id}, name='{self.name}', sku='{self.sku}')>"
