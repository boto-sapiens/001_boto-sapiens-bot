"""Telegram channel publisher service for bot announcements."""
from typing import Optional
from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest
from loguru import logger

from bot.config import settings


class TelegramPublisher:
    """Service for publishing messages to Telegram channel."""
    
    def __init__(self, bot: Bot):
        """
        Initialize Telegram publisher.
        
        Args:
            bot: Aiogram Bot instance
        """
        self.bot = bot
        self.channel_id = settings.telegram_channel_id
    
    async def post_new_species(
        self,
        bot_name: str,
        bot_username: Optional[str],
        description: str,
        creator_name: str
    ) -> bool:
        """
        Post a "New Species Discovered" announcement to the channel.
        
        Args:
            bot_name: Name of the bot
            bot_username: Username of the bot (e.g., @mybot)
            description: Bot description
            creator_name: Name of the user who added the bot
            
        Returns:
            True if posted successfully, False otherwise
        """
        # Check if channel is configured
        if not self.channel_id:
            logger.debug("Channel ID not configured, skipping channel post")
            return False
        
        # Format bot username
        if bot_username and not bot_username.startswith("@"):
            bot_username = f"@{bot_username}"
        
        # Create message text with Markdown formatting
        message_text = (
            "🧬 *New Digital Species Discovered\\!*\n\n"
            f"*Name:* {bot_name}\n"
        )
        
        if bot_username:
            # Escape special characters for MarkdownV2
            username_escaped = bot_username.replace("_", "\\_").replace("-", "\\-")
            message_text += f"*Username:* {username_escaped}\n"
        
        # Escape description for MarkdownV2
        description_escaped = (
            description
            .replace("_", "\\_")
            .replace("*", "\\*")
            .replace("[", "\\[")
            .replace("]", "\\]")
            .replace("(", "\\(")
            .replace(")", "\\)")
            .replace("~", "\\~")
            .replace("`", "\\`")
            .replace(">", "\\>")
            .replace("#", "\\#")
            .replace("+", "\\+")
            .replace("-", "\\-")
            .replace("=", "\\=")
            .replace("|", "\\|")
            .replace("{", "\\{")
            .replace("}", "\\}")
            .replace(".", "\\.")
            .replace("!", "\\!")
        )
        
        creator_escaped = (
            creator_name
            .replace("_", "\\_")
            .replace("*", "\\*")
            .replace("[", "\\[")
            .replace("]", "\\]")
            .replace("(", "\\(")
            .replace(")", "\\)")
            .replace("~", "\\~")
            .replace("`", "\\`")
            .replace(">", "\\>")
            .replace("#", "\\#")
            .replace("+", "\\+")
            .replace("-", "\\-")
            .replace("=", "\\=")
            .replace("|", "\\|")
            .replace("{", "\\{")
            .replace("}", "\\}")
            .replace(".", "\\.")
            .replace("!", "\\!")
        )
        
        message_text += (
            f"*Description:* {description_escaped}\n"
            f"*Chronicled by:* {creator_escaped}\n\n"
            "_Another unique lifeform joins our ecosystem\\!_ 🌱"
        )
        
        try:
            await self.bot.send_message(
                chat_id=self.channel_id,
                text=message_text,
                parse_mode=ParseMode.MARKDOWN_V2,
                disable_web_page_preview=True
            )
            logger.success(
                f"✅ New species announcement posted to channel: {bot_name}"
            )
            return True
            
        except TelegramBadRequest as e:
            logger.error(
                f"❌ Failed to post to channel (Bad Request): {e}. "
                "Check if bot is admin in the channel."
            )
            return False
        except Exception as e:
            logger.error(f"❌ Failed to post to channel: {e}")
            return False
    
    async def post_species_report(self, report_text: str) -> bool:
        """
        Post a general species report to the channel.
        
        Args:
            report_text: Report text to post
            
        Returns:
            True if posted successfully, False otherwise
        """
        # Check if channel is configured
        if not self.channel_id:
            logger.debug("Channel ID not configured, skipping channel post")
            return False
        
        try:
            await self.bot.send_message(
                chat_id=self.channel_id,
                text=report_text,
                disable_web_page_preview=True
            )
            logger.success("✅ Species report posted to channel")
            return True
            
        except TelegramBadRequest as e:
            logger.error(
                f"❌ Failed to post report to channel (Bad Request): {e}. "
                "Check if bot is admin in the channel."
            )
            return False
        except Exception as e:
            logger.error(f"❌ Failed to post report to channel: {e}")
            return False

