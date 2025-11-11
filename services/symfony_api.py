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
        
        # Log base URL for debugging
        logger.info(f"🔗 Symfony API base_url: {self.base_url}")
        
        # Validate base URL format
        self._validate_base_url()
    
    def _validate_base_url(self) -> None:
        """
        Validate base URL format and warn about incorrect endings.
        """
        # Check for common incorrect endings
        incorrect_endings = ['/user', '/bot', '/api/telegram/user', '/api/telegram/bot']
        
        for ending in incorrect_endings:
            if self.base_url.endswith(ending):
                logger.warning(
                    f"⚠️  Symfony API base_url ends with '{ending}' - this may cause issues!\n"
                    f"   Expected format: http://host:port/api/telegram\n"
                    f"   Current URL: {self.base_url}\n"
                    f"   Please check your SYMFONY_API_URL in .env file"
                )
                break
        
        # Check if URL looks correct
        if not self.base_url.endswith('/api/telegram'):
            logger.warning(
                f"⚠️  Symfony API base_url doesn't end with '/api/telegram'\n"
                f"   Current URL: {self.base_url}\n"
                f"   Expected format: http://host:port/api/telegram"
            )
        else:
            logger.success(f"✅ Symfony API base_url format is correct: {self.base_url}")
    
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
    
    async def test_api_connection(self) -> dict:
        """
        Test API connection with detailed response analysis.
        
        Returns:
            Dict with connection status and details
        """
        try:
            session = await self._get_session()
            test_url = f"{self.base_url}/user/12345"  # Test with dummy ID
            
            async with session.get(test_url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                content_type = response.headers.get('content-type', '')
                is_json = 'application/json' in content_type
                
                if response.status == 404:
                    # 404 is expected for non-existent user, but we want JSON response
                    try:
                        data = await response.json()
                        return {
                            "status": "success",
                            "message": "API is reachable and returns JSON",
                            "status_code": response.status,
                            "content_type": content_type,
                            "is_json": is_json,
                            "response_sample": str(data)[:200] + "..." if len(str(data)) > 200 else str(data)
                        }
                    except Exception:
                        return {
                            "status": "warning",
                            "message": "API is reachable but doesn't return JSON",
                            "status_code": response.status,
                            "content_type": content_type,
                            "is_json": is_json
                        }
                elif response.status == 200:
                    data = await response.json()
                    return {
                        "status": "success",
                        "message": "API is reachable and returns JSON",
                        "status_code": response.status,
                        "content_type": content_type,
                        "is_json": is_json,
                        "response_sample": str(data)[:200] + "..." if len(str(data)) > 200 else str(data)
                    }
                else:
                    return {
                        "status": "error",
                        "message": f"Unexpected status code: {response.status}",
                        "status_code": response.status,
                        "content_type": content_type,
                        "is_json": is_json
                    }
                    
        except aiohttp.ClientError as e:
            return {
                "status": "error",
                "message": f"Network error: {str(e)}",
                "status_code": None,
                "content_type": None,
                "is_json": False
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Unexpected error: {str(e)}",
                "status_code": None,
                "content_type": None,
                "is_json": False
            }
    
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
    
    async def get_user(self, telegram_id: str) -> dict:
        """
        Get user by Telegram ID from Symfony API.
        
        Args:
            telegram_id: Telegram user ID
            
        Returns:
            Response dict with status and user data
        """
        url = f"{self.base_url}/user/{telegram_id}"
        
        try:
            session = await self._get_session()
            async with session.get(url) as response:
                if response.status == 200:
                    response_data = await response.json()
                    logger.debug(f"User retrieved: telegram_id={telegram_id}")
                    return {
                        "status": "success",
                        "data": response_data
                    }
                elif response.status == 404:
                    logger.debug(f"User not found: telegram_id={telegram_id}")
                    return {
                        "status": "not_found",
                        "data": None
                    }
                else:
                    response_data = await response.json()
                    logger.error(
                        f"Failed to get user: status={response.status}, "
                        f"telegram_id={telegram_id}, response={response_data}"
                    )
                    return {
                        "status": "error",
                        "message": f"HTTP {response.status}: {response_data.get('message', 'Unknown error')}"
                    }
                    
        except aiohttp.ClientError as e:
            logger.error(f"Network error while getting user {telegram_id}: {e}")
            return {
                "status": "error",
                "message": f"Network error: {str(e)}"
            }
        except Exception as e:
            logger.error(f"Unexpected error while getting user {telegram_id}: {e}")
            return {
                "status": "error",
                "message": f"Unexpected error: {str(e)}"
            }
    
    async def update_user_profile(self, telegram_id: str, bio: Optional[str] = None, 
                                 interests: Optional[str] = None, full_name: Optional[str] = None,
                                 username: Optional[str] = None) -> dict:
        """
        Update user profile in Symfony API.
        
        Args:
            telegram_id: Telegram user ID
            bio: User bio (optional)
            interests: User interests (optional)
            full_name: User full name (optional)
            username: Telegram username (optional)
            
        Returns:
            Response dict with status and data
        """
        url = f"{self.base_url}/user/{telegram_id}"
        payload = {}
        
        if bio is not None:
            payload["bio"] = bio
        if interests is not None:
            payload["interests"] = interests
        if full_name is not None:
            payload["full_name"] = full_name
        if username is not None:
            payload["username"] = username
        
        try:
            session = await self._get_session()
            async with session.put(url, json=payload) as response:
                response_data = await response.json()
                
                if response.status in (200, 201):
                    logger.info(f"User profile updated: telegram_id={telegram_id}")
                    return {
                        "status": "success",
                        "data": response_data
                    }
                else:
                    logger.error(
                        f"Failed to update user profile: status={response.status}, "
                        f"telegram_id={telegram_id}, response={response_data}"
                    )
                    return {
                        "status": "error",
                        "message": f"HTTP {response.status}: {response_data.get('message', 'Unknown error')}"
                    }
                    
        except aiohttp.ClientError as e:
            logger.error(f"Network error while updating user {telegram_id}: {e}")
            return {
                "status": "error",
                "message": f"Network error: {str(e)}"
            }
        except Exception as e:
            logger.error(f"Unexpected error while updating user {telegram_id}: {e}")
            return {
                "status": "error",
                "message": f"Unexpected error: {str(e)}"
            }
    
    async def get_user_bots(self, telegram_id: str) -> dict:
        """
        Get all bots for a specific user from Symfony API.
        
        Args:
            telegram_id: Owner's Telegram user ID
            
        Returns:
            Response dict with status and bots data
        """
        url = f"{self.base_url}/user/{telegram_id}/bots"
        
        try:
            session = await self._get_session()
            async with session.get(url) as response:
                if response.status == 200:
                    response_data = await response.json()
                    logger.debug(f"User bots retrieved: telegram_id={telegram_id}")
                    return {
                        "status": "success",
                        "data": response_data
                    }
                else:
                    response_data = await response.json()
                    logger.error(
                        f"Failed to get user bots: status={response.status}, "
                        f"telegram_id={telegram_id}, response={response_data}"
                    )
                    return {
                        "status": "error",
                        "message": f"HTTP {response.status}: {response_data.get('message', 'Unknown error')}"
                    }
                    
        except aiohttp.ClientError as e:
            logger.error(f"Network error while getting user bots {telegram_id}: {e}")
            return {
                "status": "error",
                "message": f"Network error: {str(e)}"
            }
        except Exception as e:
            logger.error(f"Unexpected error while getting user bots {telegram_id}: {e}")
            return {
                "status": "error",
                "message": f"Unexpected error: {str(e)}"
            }
    
    async def get_all_users_with_bots(self) -> dict:
        """
        Get all users with their bots from Symfony API.
        
        Returns:
            Response dict with status and users data
        """
        url = f"{self.base_url}/users"
        
        try:
            session = await self._get_session()
            async with session.get(url) as response:
                if response.status == 200:
                    response_data = await response.json()
                    logger.debug("All users with bots retrieved")
                    return {
                        "status": "success",
                        "data": response_data
                    }
                else:
                    response_data = await response.json()
                    logger.error(
                        f"Failed to get all users: status={response.status}, "
                        f"response={response_data}"
                    )
                    return {
                        "status": "error",
                        "message": f"HTTP {response.status}: {response_data.get('message', 'Unknown error')}"
                    }
                    
        except aiohttp.ClientError as e:
            logger.error(f"Network error while getting all users: {e}")
            return {
                "status": "error",
                "message": f"Network error: {str(e)}"
            }
        except Exception as e:
            logger.error(f"Unexpected error while getting all users: {e}")
            return {
                "status": "error",
                "message": f"Unexpected error: {str(e)}"
            }
    
    async def delete_bot(self, bot_id: str) -> dict:
        """
        Delete a bot from Symfony API.
        
        Args:
            bot_id: Bot ID to delete
            
        Returns:
            Response dict with status
        """
        url = f"{self.base_url}/bot/{bot_id}"
        
        try:
            session = await self._get_session()
            async with session.delete(url) as response:
                if response.status in (200, 204):
                    logger.info(f"Bot deleted successfully: bot_id={bot_id}")
                    return {
                        "status": "success",
                        "data": None
                    }
                elif response.status == 404:
                    logger.warning(f"Bot not found for deletion: bot_id={bot_id}")
                    return {
                        "status": "not_found",
                        "data": None
                    }
                else:
                    response_data = await response.json()
                    logger.error(
                        f"Failed to delete bot: status={response.status}, "
                        f"bot_id={bot_id}, response={response_data}"
                    )
                    return {
                        "status": "error",
                        "message": f"HTTP {response.status}: {response_data.get('message', 'Unknown error')}"
                    }
                    
        except aiohttp.ClientError as e:
            logger.error(f"Network error while deleting bot {bot_id}: {e}")
            return {
                "status": "error",
                "message": f"Network error: {str(e)}"
            }
        except Exception as e:
            logger.error(f"Unexpected error while deleting bot {bot_id}: {e}")
            return {
                "status": "error",
                "message": f"Unexpected error: {str(e)}"
            }


# Example usage / test
async def test_symfony_api():
    """Test function to verify Symfony API connectivity."""
    api = SymfonyAPI("http://127.0.0.1:8000/api/telegram")
    
    try:
        # Test connection with detailed analysis
        connection_test = await api.test_api_connection()
        print(f"🔗 API Connection Test: {connection_test}")
        
        # Test ping
        is_alive = await api.ping()
        print(f"🏥 API Health Check: {is_alive}")
        
        # Test user upsert
        user_result = await api.upsert_user("999888777", "test_user")
        print(f"👤 Upsert User: {user_result}")
        
        # Test bot addition
        bot_result = await api.add_bot("999888777", "@dream_bot", "Experimental AI creature")
        print(f"🤖 Add Bot: {bot_result}")
        
    finally:
        await api.close()


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_symfony_api())

