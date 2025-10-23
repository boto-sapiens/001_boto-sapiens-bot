"""Daily report scheduler."""
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from aiogram import Bot
from loguru import logger

from bot.config import settings
from db.repository import UserRepository
from services.openai_service import OpenAIService


scheduler = AsyncIOScheduler(timezone=settings.timezone)
openai_service = OpenAIService()


async def send_daily_report(bot: Bot) -> None:
    """Generate and send daily Species Report to all users."""
    logger.info("Starting daily Species Report generation...")
    
    try:
        # Get all users with their bots
        users = await UserRepository.get_all_users()
        
        if not users:
            logger.warning("No users found, skipping report generation")
            return
        
        # Generate report
        report = await openai_service.generate_species_report(users)
        
        # Send report to all users
        sent_count = 0
        failed_count = 0
        
        for user in users:
            try:
                await bot.send_message(
                    chat_id=user.telegram_id,
                    text=f"🧬 **Daily Species Report**\n\n{report}",
                    parse_mode="Markdown"
                )
                sent_count += 1
            except Exception as e:
                logger.error(f"Failed to send report to user {user.telegram_id}: {e}")
                failed_count += 1
        
        logger.success(
            f"Daily report sent: {sent_count} successful, {failed_count} failed"
        )
        
    except Exception as e:
        logger.error(f"Error in daily report generation: {e}")


def setup_scheduler(bot: Bot) -> None:
    """Setup the scheduler for daily reports."""
    # Parse report time (format: HH:MM)
    hour, minute = map(int, settings.report_time.split(":"))
    
    # Add job to scheduler
    scheduler.add_job(
        send_daily_report,
        trigger=CronTrigger(hour=hour, minute=minute),
        args=[bot],
        id="daily_species_report",
        name="Daily Species Report",
        replace_existing=True
    )
    
    logger.info(
        f"Scheduler configured: Daily report at {settings.report_time} {settings.timezone}"
    )
    
    # Start scheduler
    scheduler.start()
    logger.success("Scheduler started")


def shutdown_scheduler() -> None:
    """Shutdown the scheduler."""
    if scheduler.running:
        scheduler.shutdown()
        logger.info("Scheduler stopped")

