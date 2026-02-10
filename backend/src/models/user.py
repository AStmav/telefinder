"""
User model for TeleFinder.

Represents a user account with authentication and Telegram integration.
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import Column, String, Boolean, BigInteger, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.sqlite import JSON as SQLiteJSON

from ..config.database import Base


class User(Base):
    """
    User account model.
    
    Stores user authentication data, Telegram credentials, and preferences.
    """
    
    __tablename__ = "users"
    
    # Primary Key
    id = Column(String(36), primary_key=True, index=True)  # UUID as string for SQLite
    
    # Authentication
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    
    # Telegram Integration
    telegram_user_id = Column(BigInteger, unique=True, nullable=True, index=True)
    telegram_phone = Column(String(20), nullable=True)
    telegram_session = Column(String, nullable=True)  # Encrypted Pyrogram session string
    
    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Preferences (stored as JSON for flexibility)
    notification_preferences = Column(SQLiteJSON, default={}, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_login_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    telegram_groups = relationship(
        "TelegramGroup",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
    
    filters = relationship(
        "Filter",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
    
    messages = relationship(
        "Message",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
    
    notifications = relationship(
        "Notification",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email})>"
    
    @property
    def has_telegram_auth(self) -> bool:
        """Check if user has completed Telegram authentication."""
        return self.telegram_user_id is not None and self.telegram_session is not None

