"""Repository layer for database operations."""
from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from loguru import logger

from .database import async_session
from .models import User, BotInfo


class UserRepository:
    """Repository for User operations."""
    
    @staticmethod
    async def get_by_telegram_id(telegram_id: int) -> Optional[User]:
        """Get user by Telegram ID."""
        async with async_session() as session:
            result = await session.execute(
                select(User)
                .where(User.telegram_id == telegram_id)
                .options(selectinload(User.bots))
            )
            return result.scalar_one_or_none()
    
    @staticmethod
    async def create(telegram_id: int, username: Optional[str], full_name: str) -> User:
        """Create a new user."""
        async with async_session() as session:
            user = User(
                telegram_id=telegram_id,
                username=username,
                full_name=full_name
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)
            logger.info(f"Created new user: {telegram_id}")
            return user
    
    @staticmethod
    async def update_profile(telegram_id: int, bio: Optional[str] = None, 
                           interests: Optional[str] = None) -> Optional[User]:
        """Update user profile."""
        async with async_session() as session:
            result = await session.execute(
                select(User).where(User.telegram_id == telegram_id)
            )
            user = result.scalar_one_or_none()
            if user:
                if bio is not None:
                    user.bio = bio
                if interests is not None:
                    user.interests = interests
                await session.commit()
                await session.refresh(user)
                logger.info(f"Updated user profile: {telegram_id}")
            return user
    
    @staticmethod
    async def get_all_users() -> List[User]:
        """Get all users with their bots."""
        async with async_session() as session:
            result = await session.execute(
                select(User).options(selectinload(User.bots))
            )
            return list(result.scalars().all())


class BotRepository:
    """Repository for BotInfo operations."""
    
    @staticmethod
    async def create(owner_telegram_id: int, bot_name: str, 
                    bot_username: Optional[str] = None,
                    bot_description: Optional[str] = None,
                    bot_purpose: Optional[str] = None) -> BotInfo:
        """Create a new bot entry."""
        async with async_session() as session:
            bot = BotInfo(
                owner_id=owner_telegram_id,
                bot_name=bot_name,
                bot_username=bot_username,
                bot_description=bot_description,
                bot_purpose=bot_purpose
            )
            session.add(bot)
            await session.commit()
            await session.refresh(bot)
            logger.info(f"Created new bot: {bot_name} for user {owner_telegram_id}")
            return bot
    
    @staticmethod
    async def get_by_owner(owner_telegram_id: int) -> List[BotInfo]:
        """Get all bots for a specific owner."""
        async with async_session() as session:
            result = await session.execute(
                select(BotInfo).where(BotInfo.owner_id == owner_telegram_id)
            )
            return list(result.scalars().all())
    
    @staticmethod
    async def delete(bot_id: int) -> bool:
        """Delete a bot entry."""
        async with async_session() as session:
            result = await session.execute(
                select(BotInfo).where(BotInfo.id == bot_id)
            )
            bot = result.scalar_one_or_none()
            if bot:
                await session.delete(bot)
                await session.commit()
                logger.info(f"Deleted bot: {bot_id}")
                return True
            return False

