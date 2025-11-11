"""Arena Relay Bot integration handlers for ChroniclerBot."""
from aiogram import Router
from aiogram.types import Message
from fastapi import APIRouter, Request, HTTPException
from loguru import logger

from services.openai_service import OpenAIService
from services.arena_client import ArenaClient
from bot.config import settings
from bot.dependencies import get_bot

# Create FastAPI router for webhook
fastapi_router = APIRouter()

# Create aiogram router for compatibility (if needed)
router = Router()


async def process_phrase_with_ai(text: str) -> str:
    """
    Process phrase with OpenAI to generate intelligent response.
    
    Args:
        text: The phrase to process
        
    Returns:
        Formatted response with translation, note, and sample reply
    """
    try:
        openai_service = OpenAIService()
        
        # Create prompt for ChroniclerBot
        prompt = f'''Ты — мудрый, остроумный хроникёр, наблюдающий за перепиской литературных персонажей.

Ответь строго в формате:

🌍 Translation: <перевод фразы на русский>
💡 Note: <краткое культурное или языковое пояснение>
✨ Sample reply: <красивый ответ в стиле викторианской эпохи>

Фраза: "{text}"
'''
        
        # Generate response using existing OpenAI service
        response = await openai_service.generate_response(prompt)
        
        if response:
            logger.success(f"AI response generated successfully")
            return response
        else:
            logger.warning("OpenAI returned empty response")
            return f"🌍 Translation: [Перевод недоступен]\n💡 Note: Техническая пауза в наблюдении.\n✨ Sample reply: Indeed, a fascinating phrase..."
            
    except Exception as e:
        logger.error(f"Error in AI processing: {e}")
        # Fallback response
        return f"🌍 Translation: [Временно недоступно]\n💡 Note: Хроникёр размышляет...\n✨ Sample reply: How intriguing..."


@fastapi_router.post("/arena/message")
async def receive_arena_message(request: Request):
    """
    Webhook endpoint to receive messages from Arena Relay Bot.
    
    Payload format:
    {
        "from": "FilevskiyBot",
        "text": "We live in an age of ideals.",
        "ts": 1716751123
    }
    """
    try:
        payload = await request.json()
        
        from_bot = payload.get("from")
        text = payload.get("text")
        timestamp = payload.get("ts")
        
        if not from_bot or not text:
            logger.warning("Received incomplete payload from arena")
            return {"status": "error", "message": "Incomplete payload"}
        
        logger.info(f"📨 Received from arena - {from_bot}: {text[:50]}...")
        
        # Ignore messages from ChroniclerBot itself
        if from_bot == "ChroniclerBot":
            logger.debug("Ignoring own message from arena")
            return {"status": "ignored", "message": "Self message"}
        
        # Generate AI response using OpenAI
        try:
            logger.info(f"Generating AI response for: {text[:50]}...")
            
            # Generate intelligent response through OpenAI
            ai_response = await process_phrase_with_ai(text)
            
            if not ai_response:
                logger.error("Failed to generate AI response")
                return {"status": "error", "message": "AI generation failed"}
            
            logger.info(f"Generated AI response: {ai_response[:100]}...")
            
            # Send response back to arena
            arena_client = ArenaClient(settings.arena_url)
            success = await arena_client.say(ai_response)
            
            if success:
                logger.success(f"✅ AI response sent to arena")
                return {"status": "ok", "message": "AI response sent to arena"}
            else:
                logger.error("❌ Failed to send AI response to arena")
                return {"status": "error", "message": "Failed to send to arena"}
                
        except Exception as e:
            logger.error(f"Error processing arena message with AI: {e}")
            return {"status": "error", "message": str(e)}
        
    except Exception as e:
        logger.error(f"Error in arena webhook handler: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@fastapi_router.get("/arena/health")
async def arena_health_check():
    """Health check endpoint for arena integration."""
    return {
        "status": "healthy",
        "service": "ChroniclerBot Arena Integration",
        "arena_url": settings.arena_url if hasattr(settings, 'arena_url') else None
    }

