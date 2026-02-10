"""
Database configuration and session management for SQLite.

Provides SQLAlchemy engine, session factory, and database dependency for FastAPI.
"""

from typing import Generator
from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from .settings import get_settings

settings = get_settings()

# SQLite-specific configuration
# - check_same_thread=False allows multiple threads (needed for FastAPI)
# - StaticPool keeps connection alive for SQLite
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    echo=settings.debug  # Log SQL queries in debug mode
)


# Enable foreign key constraints for SQLite
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_conn, connection_record):
    """Enable foreign key constraints on each connection."""
    cursor = dbapi_conn.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for ORM models
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    Database session dependency for FastAPI.
    
    Yields a database session and ensures it's closed after request.
    
    Usage:
        @app.get("/items/")
        def read_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
    
    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """
    Initialize database by creating all tables.
    
    This should be called on application startup.
    In production, use Alembic migrations instead.
    """
    Base.metadata.create_all(bind=engine)


def get_db_session() -> Session:
    """
    Get a database session (for non-FastAPI contexts).
    
    Returns:
        Session: SQLAlchemy database session
        
    Note:
        Caller is responsible for closing the session.
    """
    return SessionLocal()

