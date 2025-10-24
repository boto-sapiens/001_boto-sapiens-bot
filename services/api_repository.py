"""API repository layer for Symfony API operations."""
from typing import Optional, List, Dict, Any
from datetime import datetime
from loguru import logger

from bot.dependencies import get_symfony_api


class ApiUserRepository:
    """Repository for User operations via Symfony API."""
    
    @staticmethod
    async def get_by_telegram_id(telegram_id: int) -> Optional[Dict[str, Any]]:
        """Get user by Telegram ID."""
        symfony_api = get_symfony_api()
        if not symfony_api:
            logger.error("Symfony API not available")
            return None
        
        result = await symfony_api.get_user(str(telegram_id))
        
        if result.get("status") == "success":
            return result.get("data")
        elif result.get("status") == "not_found":
            return None
        else:
            logger.error(f"Failed to get user {telegram_id}: {result.get('message')}")
            return None
    
    @staticmethod
    async def create(telegram_id: int, username: Optional[str], full_name: str) -> Optional[Dict[str, Any]]:
        """Create a new user."""
        symfony_api = get_symfony_api()
        if not symfony_api:
            logger.error("Symfony API not available")
            return None
        
        result = await symfony_api.upsert_user(
            telegram_id=str(telegram_id),
            username=username
        )
        
        if result.get("status") == "success":
            # Update full name if provided
            if full_name:
                update_result = await symfony_api.update_user_profile(
                    telegram_id=str(telegram_id),
                    full_name=full_name
                )
                if update_result.get("status") != "success":
                    logger.warning(f"Failed to update full name for user {telegram_id}")
            
            logger.info(f"Created new user: {telegram_id}")
            return result.get("data")
        else:
            logger.error(f"Failed to create user {telegram_id}: {result.get('message')}")
            return None
    
    @staticmethod
    async def update_profile(telegram_id: int, bio: Optional[str] = None, 
                           interests: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Update user profile."""
        symfony_api = get_symfony_api()
        if not symfony_api:
            logger.error("Symfony API not available")
            return None
        
        result = await symfony_api.update_user_profile(
            telegram_id=str(telegram_id),
            bio=bio,
            interests=interests
        )
        
        if result.get("status") == "success":
            logger.info(f"Updated user profile: {telegram_id}")
            return result.get("data")
        else:
            logger.error(f"Failed to update user profile {telegram_id}: {result.get('message')}")
            return None
    
    @staticmethod
    async def get_all_users() -> List[Dict[str, Any]]:
        """Get all users with their bots."""
        symfony_api = get_symfony_api()
        if not symfony_api:
            logger.error("Symfony API not available")
            return []
        
        result = await symfony_api.get_all_users_with_bots()
        
        if result.get("status") == "success":
            users_data = result.get("data", [])
            # Transform API response to match expected format
            transformed_users = []
            for user_data in users_data:
                transformed_user = {
                    "telegram_id": user_data.get("telegram_id"),
                    "username": user_data.get("username"),
                    "full_name": user_data.get("full_name"),
                    "bio": user_data.get("bio"),
                    "interests": user_data.get("interests"),
                    "created_at": user_data.get("created_at"),
                    "updated_at": user_data.get("updated_at"),
                    "bots": user_data.get("bots", [])
                }
                transformed_users.append(transformed_user)
            
            return transformed_users
        else:
            logger.error(f"Failed to get all users: {result.get('message')}")
            return []


class ApiBotRepository:
    """Repository for BotInfo operations via Symfony API."""
    
    @staticmethod
    async def create(owner_telegram_id: int, bot_name: str, 
                    bot_username: Optional[str] = None,
                    bot_description: Optional[str] = None,
                    bot_purpose: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Create a new bot entry."""
        symfony_api = get_symfony_api()
        if not symfony_api:
            logger.error("Symfony API not available")
            return None
        
        # Use the existing add_bot method
        result = await symfony_api.add_bot(
            telegram_id=str(owner_telegram_id),
            bot_username=bot_username or "",
            description=bot_description or ""
        )
        
        if result.get("status") == "success":
            bot_data = result.get("data", {})
            # Add additional fields that might not be in the API response
            bot_data.update({
                "bot_name": bot_name,
                "bot_purpose": bot_purpose,
                "owner_id": owner_telegram_id,
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            })
            
            logger.info(f"Created new bot: {bot_name} for user {owner_telegram_id}")
            return bot_data
        else:
            logger.error(f"Failed to create bot {bot_name}: {result.get('message')}")
            return None
    
    @staticmethod
    async def get_by_owner(owner_telegram_id: int) -> List[Dict[str, Any]]:
        """Get all bots for a specific owner."""
        symfony_api = get_symfony_api()
        if not symfony_api:
            logger.error("Symfony API not available")
            return []
        
        result = await symfony_api.get_user_bots(str(owner_telegram_id))
        
        if result.get("status") == "success":
            bots_data = result.get("data", [])
            # Transform API response to match expected format
            transformed_bots = []
            for bot_data in bots_data:
                transformed_bot = {
                    "id": bot_data.get("id"),
                    "owner_id": owner_telegram_id,
                    "bot_name": bot_data.get("bot_name", ""),
                    "bot_username": bot_data.get("bot_username"),
                    "bot_description": bot_data.get("description", ""),
                    "bot_purpose": bot_data.get("bot_purpose", ""),
                    "created_at": bot_data.get("created_at"),
                    "updated_at": bot_data.get("updated_at")
                }
                transformed_bots.append(transformed_bot)
            
            return transformed_bots
        else:
            logger.error(f"Failed to get bots for user {owner_telegram_id}: {result.get('message')}")
            return []
    
    @staticmethod
    async def delete(bot_id: int) -> bool:
        """Delete a bot entry."""
        symfony_api = get_symfony_api()
        if not symfony_api:
            logger.error("Symfony API not available")
            return False
        
        result = await symfony_api.delete_bot(str(bot_id))
        
        if result.get("status") in ("success", "not_found"):
            logger.info(f"Deleted bot: {bot_id}")
            return True
        else:
            logger.error(f"Failed to delete bot {bot_id}: {result.get('message')}")
            return False

