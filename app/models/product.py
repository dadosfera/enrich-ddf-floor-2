"""
Product and classification-related database models.
"""

from sqlalchemy import (
    Column, String, Text, Integer, Boolean, Numeric
)

from app.models.base import Base, UUIDMixin, TimestampMixin


class Product(Base, UUIDMixin, TimestampMixin):
    """Product information and classification model."""
    
    __tablename__ = "products"
    
    name = Column(String(500), nullable=False, index=True)
    description = Column(Text)
    ncm_code = Column(String(20), index=True)
    hs_code = Column(String(20), index=True)
    cnae_code = Column(String(20), index=True)
    category = Column(String(255))
    brand = Column(String(255))
    model = Column(String(255))
    confidence_score = Column(Numeric(3, 2), default=0.0)
    
    def __repr__(self) -> str:
        return f"<Product(name='{self.name}', ncm='{self.ncm_code}')>"


class NCMCode(Base):
    """NCM (Mercosur Common Nomenclature) classification reference."""
    
    __tablename__ = "ncm_codes"
    
    code = Column(String(20), primary_key=True)
    description = Column(Text, nullable=False)
    parent_code = Column(String(20))
    level = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column("created_at", nullable=False)
    
    def __repr__(self) -> str:
        return f"<NCMCode(code='{self.code}', level={self.level})>"


class CNAECode(Base):
    """CNAE (National Classification of Economic Activities) reference."""
    
    __tablename__ = "cnae_codes"
    
    code = Column(String(20), primary_key=True)
    description = Column(Text, nullable=False)
    section = Column(String(10))
    division = Column(String(10))
    group_code = Column(String(10))
    class_code = Column(String(10))
    is_active = Column(Boolean, default=True)
    created_at = Column("created_at", nullable=False)
    
    def __repr__(self) -> str:
        return f"<CNAECode(code='{self.code}', section='{self.section}')>" 