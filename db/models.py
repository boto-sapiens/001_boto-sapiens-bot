"""Database models for boto-sapiens."""
from datetime import datetime
from typing import List

from sqlalchemy import BigInteger, String, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base class for all models."""
    pass


class User(Base):
    """User model representing Telegram users."""
    
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, index=True)
    username: Mapped[str] = mapped_column(String(255), nullable=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # User information
    bio: Mapped[str] = mapped_column(Text, nullable=True)
    interests: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
    
    # Relationships
    bots: Mapped[List["BotInfo"]] = relationship(
        "BotInfo", 
        back_populates="owner",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return f"<User(telegram_id={self.telegram_id}, username={self.username})>"


class BotInfo(Base):
    """Bot information model."""
    
    __tablename__ = "bot_info"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    owner_id: Mapped[int] = mapped_column(
        BigInteger, 
        ForeignKey("users.telegram_id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # Bot details
    bot_name: Mapped[str] = mapped_column(String(255), nullable=False)
    bot_username: Mapped[str] = mapped_column(String(255), nullable=True)
    bot_description: Mapped[str] = mapped_column(Text, nullable=True)
    bot_purpose: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
    
    # Relationships
    owner: Mapped["User"] = relationship("User", back_populates="bots")
    
    def __repr__(self) -> str:
        return f"<BotInfo(bot_name={self.bot_name}, owner_id={self.owner_id})>"

