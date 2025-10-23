"""Symfony API client for synchronizing user and bot data."""
from typing import Optional
import aiohttp
from loguru import logger


class SymfonyAPI:
    """Client for interacting with Symfony REST API."""
    
    def __init__(self, base_url: str):
        """
        Initialize Symfony API client.
        
        Args:
            base_url: Base URL for Symfony API (e.g., http://127.0.0.1:8000/api/telegram)
        """
        self.base_url = base_url.rstrip('/')
        self._session: Optional[aiohttp.ClientSession] = None
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session."""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=10)
            )
        return self._session
    
    async def close(self) -> None:
        """Close aiohttp session."""
        if self._session and not self._session.closed:
            await self._session.close()
            logger.info("Symfony API session closed")
    
    async def ping(self) -> bool:
        """
        Check if Symfony API is available.
        
        Returns:
            True if API is reachable, False otherwise
        """
        try:
            session = await self._get_session()
            async with session.get(f"{self.base_url}/health", timeout=aiohttp.ClientTimeout(total=5)) as response:
                logger.debug(f"Symfony API ping status: {response.status}")
                return response.status == 200
        except aiohttp.ClientError as e:
            logger.warning(f"Symfony API ping failed: {e}")
            return False
        except Exception as e:
            logger.warning(f"Unexpected error during Symfony API ping: {e}")
            return False
    
    async def upsert_user(self, telegram_id: str, username: Optional[str] = None) -> dict:
        """
        Create or update user in Symfony API.
        
        Args:
            telegram_id: Telegram user ID
            username: Telegram username (optional)
            
        Returns:
            Response dict with status and data
        """
        url = f"{self.base_url}/user"
        payload = {
            "telegram_id": str(telegram_id),
            "username": username or ""
        }
        
        try:
            session = await self._get_session()
            async with session.post(url, json=payload) as response:
                response_data = await response.json()
                
                if response.status in (200, 201):
                    logger.info(f"User upserted successfully: telegram_id={telegram_id}, username={username}")
                    return {
                        "status": "success",
                        "data": response_data
                    }
                else:
                    logger.error(
                        f"Failed to upsert user: status={response.status}, "
                        f"telegram_id={telegram_id}, response={response_data}"
                    )
                    return {
                        "status": "error",
                        "message": f"HTTP {response.status}: {response_data.get('message', 'Unknown error')}"
                    }
                    
        except aiohttp.ClientError as e:
            logger.error(f"Network error while upserting user {telegram_id}: {e}")
            return {
                "status": "error",
                "message": f"Network error: {str(e)}"
            }
        except Exception as e:
            logger.error(f"Unexpected error while upserting user {telegram_id}: {e}")
            return {
                "status": "error",
                "message": f"Unexpected error: {str(e)}"
            }
    
    async def add_bot(self, telegram_id: str, bot_username: str, description: str) -> dict:
        """
        Add a new Telegram bot to Symfony API.
        
        Args:
            telegram_id: Owner's Telegram user ID
            bot_username: Bot's username (e.g., @mybot)
            description: Bot description
            
        Returns:
            Response dict with status and data
        """
        url = f"{self.base_url}/bot"
        payload = {
            "telegram_id": str(telegram_id),
            "bot_username": bot_username,
            "description": description
        }
        
        try:
            session = await self._get_session()
            async with session.post(url, json=payload) as response:
                response_data = await response.json()
                
                if response.status in (200, 201):
                    logger.info(
                        f"Bot added successfully: telegram_id={telegram_id}, "
                        f"bot_username={bot_username}"
                    )
                    return {
                        "status": "success",
                        "data": response_data
                    }
                else:
                    logger.error(
                        f"Failed to add bot: status={response.status}, "
                        f"telegram_id={telegram_id}, bot_username={bot_username}, "
                        f"response={response_data}"
                    )
                    return {
                        "status": "error",
                        "message": f"HTTP {response.status}: {response_data.get('message', 'Unknown error')}"
                    }
                    
        except aiohttp.ClientError as e:
            logger.error(
                f"Network error while adding bot {bot_username} for user {telegram_id}: {e}"
            )
            return {
                "status": "error",
                "message": f"Network error: {str(e)}"
            }
        except Exception as e:
            logger.error(
                f"Unexpected error while adding bot {bot_username} for user {telegram_id}: {e}"
            )
            return {
                "status": "error",
                "message": f"Unexpected error: {str(e)}"
            }


# Example usage / test
async def test_symfony_api():
    """Test function to verify Symfony API connectivity."""
    api = SymfonyAPI("http://127.0.0.1:8000/api/telegram")
    
    try:
        # Test ping
        is_alive = await api.ping()
        print(f"API Alive: {is_alive}")
        
        # Test user upsert
        user_result = await api.upsert_user("999888777", "test_user")
        print(f"Upsert User: {user_result}")
        
        # Test bot addition
        bot_result = await api.add_bot("999888777", "@dream_bot", "Experimental AI creature")
        print(f"Add Bot: {bot_result}")
        
    finally:
        await api.close()


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_symfony_api())

