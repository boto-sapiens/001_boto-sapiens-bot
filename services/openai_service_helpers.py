"""Helper methods for OpenAI service."""
from openai import AsyncOpenAI
import os


async def generate_simple_response(prompt: str, model: str = "gpt-4") -> str:
    """
    Generate a simple text response using OpenAI.
    
    Args:
        prompt: The prompt to send to OpenAI
        model: Model to use (default: gpt-4)
        
    Returns:
        Generated response text
    """
    client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    try:
        response = await client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are the ChroniclerBot, an AI observer of digital ecosystems."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        raise Exception(f"OpenAI API error: {e}")

