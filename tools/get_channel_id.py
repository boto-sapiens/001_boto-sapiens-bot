"""Utility to discover and save Telegram channel ID to .env file."""
import asyncio
import sys
from pathlib import Path
from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest, TelegramUnauthorizedError
from dotenv import set_key, find_dotenv
from loguru import logger


# Configure loguru
logger.remove()
logger.add(
    sys.stdout,
    format="<level>{level: <8}</level> | <level>{message}</level>",
    level="INFO"
)


def extract_username_from_input(user_input: str) -> str:
    """
    Extract channel username from various input formats.
    
    Args:
        user_input: User input (URL, username with/without @, etc.)
        
    Returns:
        Clean username with @ prefix
    """
    user_input = user_input.strip()
    
    # Handle URL formats
    if "t.me/" in user_input:
        # Extract username from URL
        username = user_input.split("t.me/")[-1]
        # Remove trailing slashes
        username = username.rstrip("/")
        # Remove query parameters
        if "?" in username:
            username = username.split("?")[0]
    else:
        username = user_input
    
    # Add @ if not present
    if not username.startswith("@"):
        username = f"@{username}"
    
    return username


async def get_channel_info(bot_token: str, channel_input: str) -> dict:
    """
    Get channel information using bot token and channel username.
    
    Args:
        bot_token: Telegram bot token
        channel_input: Channel username, URL, or identifier
        
    Returns:
        Dictionary with channel info (id, title, type)
    """
    bot = Bot(token=bot_token)
    
    try:
        # Extract clean username
        username = extract_username_from_input(channel_input)
        
        logger.info(f"Attempting to access channel: {username}")
        
        # Get chat info
        chat = await bot.get_chat(username)
        
        return {
            "id": chat.id,
            "title": chat.title or chat.full_name or "Unknown",
            "type": chat.type,
            "username": chat.username
        }
        
    except TelegramUnauthorizedError:
        logger.error("❌ Invalid bot token!")
        return None
    except TelegramBadRequest as e:
        logger.error(f"❌ Could not access channel: {e}")
        logger.info("💡 Possible reasons:")
        logger.info("   1. Bot is not a member/admin of the channel")
        logger.info("   2. Channel username is incorrect")
        logger.info("   3. Channel is private (use public channels or add bot first)")
        return None
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        return None
    finally:
        await bot.session.close()


def save_channel_id_to_env(channel_id: int) -> bool:
    """
    Save channel ID to .env file.
    
    Args:
        channel_id: Telegram channel ID
        
    Returns:
        True if saved successfully, False otherwise
    """
    try:
        # Find .env file
        env_file = find_dotenv()
        
        if not env_file:
            # Create .env in current directory
            env_file = Path.cwd() / ".env"
            logger.warning("⚠️  .env file not found, creating new one")
        
        # Save channel ID
        set_key(env_file, "TELEGRAM_CHANNEL_ID", str(channel_id))
        logger.success(f"✅ TELEGRAM_CHANNEL_ID saved to {env_file}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to save to .env: {e}")
        return False


async def main():
    """Main function to run the channel ID discovery utility."""
    logger.info("🔍 Telegram Channel ID Discovery Utility")
    logger.info("=" * 50)
    logger.info("")
    logger.info("💡 Supported formats:")
    logger.info("   - @BotoSapiens")
    logger.info("   - BotoSapiens")
    logger.info("   - https://t.me/BotoSapiens")
    logger.info("")
    
    # Get channel username/URL
    print()
    channel_input = input("Enter your channel username or URL: ").strip()
    
    if not channel_input:
        logger.error("❌ Channel username cannot be empty!")
        return
    
    # Get bot token
    bot_token = input("Enter your bot token: ").strip()
    
    if not bot_token:
        logger.error("❌ Bot token cannot be empty!")
        return
    
    print()
    logger.info("🔄 Fetching channel information...")
    
    # Get channel info
    channel_info = await get_channel_info(bot_token, channel_input)
    
    if not channel_info:
        logger.error("❌ Failed to get channel information")
        return
    
    # Display channel info
    print()
    logger.info("=" * 50)
    logger.success(f"Channel title: {channel_info['title']}")
    logger.success(f"Channel type: {channel_info['type']}")
    if channel_info.get('username'):
        logger.success(f"Channel username: @{channel_info['username']}")
    logger.success(f"Channel ID: {channel_info['id']}")
    logger.info("=" * 50)
    print()
    
    # Save to .env
    if save_channel_id_to_env(channel_info['id']):
        logger.success("🎉 Setup complete! You can now use channel publishing in your bot.")
    else:
        logger.error("❌ Setup incomplete. Please manually add TELEGRAM_CHANNEL_ID to your .env file.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("⚠️  Operation cancelled by user")
        sys.exit(0)
    except Exception as e:
        logger.critical(f"💥 Critical error: {e}")
        sys.exit(1)

