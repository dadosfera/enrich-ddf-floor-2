"""Database models package."""

from database.models.base import BaseModel
from database.models.company import Company
from database.models.contact import Contact
from database.models.product import Product


__all__ = ["BaseModel", "Company", "Contact", "Product"]
