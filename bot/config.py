"""Configuration module for boto-sapiens bot."""
import base64
import os
from typing import Optional
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from loguru import logger


class Settings(BaseSettings):
    """Application settings."""
    
    # Telegram Bot
    bot_token: str
    
    # Database removed - using Symfony API exclusively
    
    # OpenAI (Base64 encoded)
    openai_api_key_base64: str
    _openai_api_key_decoded: Optional[str] = None
    
    # Symfony API
    symfony_api_url: str = "http://127.0.0.1:8000/api/telegram"
    
    # Telegram Channel (optional)
    telegram_channel_id: Optional[int] = None
    
    # Target Chat ID for message monitoring (ChroniclerBot)
    target_chat_id: Optional[int] = None
    
    # Scheduler
    report_time: str = "09:00"
    timezone: str = "UTC"
    
    # Logging
    log_level: str = "INFO"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )
    
    @field_validator('openai_api_key_base64')
    @classmethod
    def decode_openai_key(cls, v: str) -> str:
        """Validate and decode OpenAI API key from Base64."""
        try:
            # Decode from Base64
            decoded_bytes = base64.b64decode(v)
            decoded_key = decoded_bytes.decode('utf-8')
            
            # Basic validation - OpenAI keys start with 'sk-'
            if not decoded_key.startswith('sk-'):
                logger.warning(
                    "⚠️ Decoded OpenAI API key doesn't start with 'sk-'. "
                    "This might be an invalid key."
                )
            
            logger.success("✅ OpenAI API key successfully decoded from Base64")
            return v
            
        except base64.binascii.Error as e:
            logger.error(f"❌ Failed to decode OpenAI API key from Base64: {e}")
            raise ValueError(
                "Invalid Base64 encoding for OPENAI_API_KEY_BASE64. "
                "Please check your .env file."
            )
        except UnicodeDecodeError as e:
            logger.error(f"❌ Failed to decode OpenAI API key to UTF-8: {e}")
            raise ValueError(
                "Decoded Base64 value is not valid UTF-8 text. "
                "Please check your .env file."
            )
    
    @property
    def openai_api_key(self) -> str:
        """Get decoded OpenAI API key."""
        if self._openai_api_key_decoded is None:
            decoded_bytes = base64.b64decode(self.openai_api_key_base64)
            self._openai_api_key_decoded = decoded_bytes.decode('utf-8')
        return self._openai_api_key_decoded


def decode_openai_key():
    """Decode OpenAI API key from Base64 and set it in environment."""
    try:
        # Read the Base64 encoded key from environment
        encoded_key = os.getenv("OPENAI_API_KEY_BASE64")
        if not encoded_key:
            logger.error("❌ OPENAI_API_KEY_BASE64 environment variable not found")
            return False
        
        # Decode from Base64
        decoded_bytes = base64.b64decode(encoded_key)
        decoded_key = decoded_bytes.decode('utf-8')
        
        # Basic validation - OpenAI keys start with 'sk-'
        if not decoded_key.startswith('sk-'):
            logger.warning(
                "⚠️ Decoded OpenAI API key doesn't start with 'sk-'. "
                "This might be an invalid key."
            )
        
        # Set the decoded key in environment
        os.environ["OPENAI_API_KEY"] = decoded_key
        logger.success("✅ OpenAI API key successfully decoded and set in environment")
        return True
        
    except base64.binascii.Error as e:
        logger.error(f"❌ Failed to decode OpenAI API key from Base64: {e}")
        return False
    except UnicodeDecodeError as e:
        logger.error(f"❌ Failed to decode OpenAI API key to UTF-8: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ Unexpected error while decoding OpenAI API key: {e}")
        return False


# Global settings instance
settings = Settings()

