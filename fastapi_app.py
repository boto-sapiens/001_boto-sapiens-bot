"""FastAPI application for ChroniclerBot webhooks."""
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn
from loguru import logger

from bot.config import settings
from handlers.arena_handlers import fastapi_router
from services.arena_client import ArenaClient


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan."""
    logger.info("🚀 ChroniclerBot FastAPI starting up...")
    
    # Register in Arena Relay Bot if enabled
    if settings.arena_enabled:
        arena_client = ArenaClient(settings.arena_url)
        
        # Check arena health
        is_healthy = await arena_client.check_health()
        if is_healthy:
            # Register webhook (using actual container name: boto-chronicler)
            webhook_url = f"http://boto-chronicler:{settings.arena_webhook_port}/arena/message"
            success = await arena_client.register(webhook_url)
            if success:
                logger.success(f"✅ Registered in Arena with webhook: {webhook_url}")
            else:
                logger.warning("⚠️  Failed to register in Arena")
        else:
            logger.warning("⚠️  Arena Relay Bot is not available")
    
    logger.success("✅ FastAPI startup completed")
    
    yield
    
    logger.info("🛑 ChroniclerBot FastAPI shutting down...")
    logger.success("✅ FastAPI shutdown completed")


# Create FastAPI app
app = FastAPI(
    title="ChroniclerBot API",
    description="Webhook API for Arena Relay Bot integration",
    version="1.0.0",
    lifespan=lifespan
)

# Include arena handlers
app.include_router(fastapi_router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "service": "ChroniclerBot API",
        "status": "running",
        "arena_enabled": settings.arena_enabled,
        "arena_url": settings.arena_url
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "ChroniclerBot API",
        "version": "1.0.0"
    }


if __name__ == "__main__":
    uvicorn.run(
        "fastapi_app:app",
        host="0.0.0.0",
        port=settings.arena_webhook_port,
        reload=False
    )

