"""
Database connection and session management using SQLAlchemy async.
"""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncSession, create_async_engine, async_sessionmaker
)

from app.core.config import settings
from app.models.base import Base

# Create async engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
    pool_pre_ping=True,
    pool_recycle=3600,
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency to get database session.
    
    Yields:
        AsyncSession: Database session
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db() -> None:
    """
    Initialize database tables.
    
    This function creates all tables defined in the models.
    Should be called during application startup.
    """
    async with engine.begin() as conn:
        # Import all models to ensure they are registered with SQLAlchemy
        # These imports are necessary for table creation
        from app.models import user, company, contact, product, enrichment  # noqa
        
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)


async def close_db() -> None:
    """
    Close database connections.
    
    Should be called during application shutdown.
    """
    await engine.dispose()


# Database health check
async def check_db_health() -> bool:
    """
    Check database connectivity.
    
    Returns:
        bool: True if database is accessible, False otherwise
    """
    try:
        async with AsyncSessionLocal() as session:
            await session.execute("SELECT 1")
            return True
    except Exception:
        return False 