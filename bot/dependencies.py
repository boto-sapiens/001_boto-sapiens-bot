"""Shared dependencies for the bot application."""
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from aiogram import Bot
    from services.symfony_api import SymfonyAPI


# Global Symfony API instance
symfony_api: Optional["SymfonyAPI"] = None

# Global Bot instance
_bot_instance: Optional["Bot"] = None


def get_symfony_api() -> Optional["SymfonyAPI"]:
    """Get the global Symfony API instance."""
    return symfony_api


def set_symfony_api(api: "SymfonyAPI") -> None:
    """Set the global Symfony API instance."""
    global symfony_api
    symfony_api = api


def get_bot() -> Optional["Bot"]:
    """Get the global Bot instance."""
    return _bot_instance


def set_bot(bot: "Bot") -> None:
    """Set the global Bot instance."""
    global _bot_instance
    _bot_instance = bot

