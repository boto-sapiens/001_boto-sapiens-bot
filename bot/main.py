"""Main entry point for boto-sapiens Telegram bot."""
import asyncio
import sys
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from loguru import logger

from bot.config import settings
from bot import dependencies
from db.database import init_db, close_db
from handlers import user_router
from scheduler import setup_scheduler, shutdown_scheduler
from services.symfony_api import SymfonyAPI


# Configure loguru
logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
    level=settings.log_level
)
logger.add(
    "logs/bot.log",
    rotation="1 day",
    retention="7 days",
    level=settings.log_level,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function} - {message}"
)


async def on_startup(bot: Bot) -> None:
    """Execute on bot startup."""
    logger.info("🧬 boto-sapiens is starting up...")
    
    # Initialize database
    await init_db()
    
    # Initialize Symfony API client
    symfony_api = SymfonyAPI(settings.symfony_api_url)
    dependencies.set_symfony_api(symfony_api)
    logger.info(f"Symfony API client initialized: {settings.symfony_api_url}")
    
    # Setup scheduler for daily reports
    setup_scheduler(bot)
    
    logger.success("✅ Bot startup completed successfully")


async def on_shutdown() -> None:
    """Execute on bot shutdown."""
    logger.info("🛑 boto-sapiens is shutting down...")
    
    # Shutdown scheduler
    shutdown_scheduler()
    
    # Close Symfony API client
    symfony_api = dependencies.get_symfony_api()
    if symfony_api:
        await symfony_api.close()
    
    # Close database connections
    await close_db()
    
    logger.success("✅ Bot shutdown completed")


async def main() -> None:
    """Main function to run the bot."""
    logger.info("🚀 Initializing boto-sapiens bot...")
    
    # Initialize bot and dispatcher
    bot = Bot(token=settings.bot_token)
    dependencies.set_bot(bot)
    dp = Dispatcher(storage=MemoryStorage())
    
    # Register routers
    dp.include_router(user_router)
    
    # Register startup/shutdown handlers
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    
    try:
        # Start polling
        logger.info("📡 Starting polling...")
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except Exception as e:
        logger.error(f"❌ Error during polling: {e}")
        raise
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("⚠️ Bot stopped by user")
    except Exception as e:
        logger.critical(f"💥 Critical error: {e}")
        sys.exit(1)
