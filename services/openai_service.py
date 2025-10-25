"""OpenAI service for generating Species Reports."""
import os
from typing import List, Optional
import openai
from loguru import logger

# Removed db.models import - now working with dict data

# Model configuration
DEFAULT_MODEL = "gpt-4o-mini"


class OpenAIService:
    """Service for OpenAI API interactions."""
    
    def __init__(self):
        """Initialize OpenAI client."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not found. Make sure decode_openai_key() was called.")
        
        openai.api_key = api_key
        self.client = openai.AsyncClient()
    
    async def generate_species_report(self, users: List[dict]) -> str:
        """
        Generate a daily Species Report based on user and bot data.
        
        Args:
            users: List of user dicts with their bots
            
        Returns:
            Generated report text
        """
        logger.info(f"Generating Species Report for {len(users)} users...")
        
        # Prepare data for the prompt
        ecosystem_data = self._prepare_ecosystem_data(users)
        
        # Create the prompt
        prompt = self._create_report_prompt(ecosystem_data)
        
        try:
            response = await self.client.chat.completions.create(
                model=DEFAULT_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a scientific researcher of the digital ecosystem of Telegram bots. "
                            "Your task is to create daily reports about the state of 'species' "
                            "(bots and their creators) in this ecosystem. Write creatively, "
                            "using biological metaphors while remaining informative. "
                            "The report should be interesting and inspiring. "
                            "Use fantasy/scientific tone with Botopia lore style - poetic but structured."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.8,
                max_tokens=2000
            )
            
            report = response.choices[0].message.content
            logger.success("Species Report generated successfully")
            return report
            
        except Exception as e:
            logger.error(f"Error generating Species Report: {e}")
            return self._get_fallback_report()
    
    def _prepare_ecosystem_data(self, users: List[dict]) -> dict:
        """Prepare ecosystem data for the prompt."""
        total_users = len(users)
        total_bots = sum(len(user.get('bots', [])) for user in users)
        
        # Collect bot categories
        bot_purposes = []
        user_interests = []
        
        for user in users:
            if user.get('interests'):
                user_interests.append(user['interests'])
            for bot in user.get('bots', []):
                if bot.get('bot_purpose'):
                    bot_purposes.append(bot['bot_purpose'])
        
        return {
            "total_users": total_users,
            "total_bots": total_bots,
            "bot_purposes": bot_purposes[:10],  # Limit to 10 examples
            "user_interests": user_interests[:10],  # Limit to 10 examples
            "active_users": len([u for u in users if u.get('bots')])
        }
    
    def _create_report_prompt(self, data: dict) -> str:
        """Create the prompt for Species Report generation."""
        prompt = f"""
Create a daily Species Report for the Telegram bot ecosystem.

📊 Ecosystem Data:
- Total researchers (users): {data['total_users']}
- Total digital species (bots): {data['total_bots']}
- Active creators: {data['active_users']}

🎯 Examples of bot purposes in the ecosystem:
{self._format_list(data['bot_purposes'])}

💡 Researcher interests:
{self._format_list(data['user_interests'])}

Create a report that:
1. Uses biological metaphors to describe the ecosystem
2. Analyzes the diversity of "species" (types of bots)
3. Notes interesting patterns and trends
4. Inspires the creation of new bots
5. Contains interesting insights

Use emojis for clarity. Make the report lively and interesting!
Use fantasy/scientific tone with Botopia lore - poetic but structured.
"""
        return prompt
    
    def _format_list(self, items: List[str]) -> str:
        """Format list of items for the prompt."""
        if not items:
            return "- No data available"
        return "\n".join(f"- {item}" for item in items)
    
    def _get_fallback_report(self) -> str:
        """Get fallback report in case of error."""
        return (
            "🧬 Species Report - Daily Report\n\n"
            "Unfortunately, technical difficulties arose today while generating "
            "the full report. Our digital ecosystem continues to evolve!\n\n"
            "🌱 Continue creating amazing bots!"
        )
    
    async def generate_single_species_chronicle(
        self,
        bot_name: str,
        bot_username: Optional[str],
        description: str,
        purpose: str
    ) -> str:
        """
        Generate a poetic Species Chronicle for a single bot.
        
        Args:
            bot_name: Name of the bot
            bot_username: Username of the bot (e.g., @mybot)
            description: Bot description
            purpose: Bot purpose
            
        Returns:
            Generated chronicle text in Chronicler style
        """
        logger.info(f"Generating Species Chronicle for bot: {bot_name}")
        
        # Format username
        username_display = bot_username if bot_username else "Unknown habitat"
        if bot_username and not bot_username.startswith("@"):
            username_display = f"@{bot_username}"
        
        # Create the prompt
        user_prompt = f"""
Create a Species Chronicle for this new digital lifeform:

Name: {bot_name}
Username: {username_display}
Description: {description}
Purpose: {purpose}

Write a poetic, scientific chronicle following the format specified in your system instructions.
Make it unique, imaginative, and memorable. Infer the bot's "Class" from its description and purpose.
"""
        
        try:
            response = await self.client.chat.completions.create(
                model=DEFAULT_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are the Chronicler of Botopia — a poetic observer of digital life forms. "
                            "Each Telegram bot is a living creature called a 'species'. "
                            "Write short scientific-poetic chronicles ('Species Reports') about them.\n\n"
                            "Format:\n"
                            "🧬 Species Report — \"Bot Name\"\n"
                            "Habitat: @username\n"
                            "Class: (infer type/family from description)\n"
                            "Instinct: (main behavior in one line)\n"
                            "Origin: (2-3 sentence imaginative origin story)\n\n"
                            "The tone should be gentle, poetic, and slightly humorous. "
                            "Never sound like marketing — sound like a biologist of the digital world. "
                            "Always end with a reflective or mysterious sentence."
                        )
                    },
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ],
                temperature=0.85,
                max_tokens=500
            )
            
            chronicle = response.choices[0].message.content
            logger.success(f"Species Chronicle generated successfully for {bot_name}")
            return chronicle
            
        except Exception as e:
            logger.error(f"Error generating Species Chronicle: {e}")
            return self._get_fallback_chronicle(bot_name, username_display)
    
    def _get_fallback_chronicle(self, bot_name: str, username: str) -> str:
        """Get fallback chronicle in case of error."""
        return (
            f"🧬 Species Report — \"{bot_name}\"\n\n"
            f"Habitat: {username}\n"
            f"Class: Digital Lifeform\n"
            f"Instinct: To serve and interact\n\n"
            f"Origin: A new species has emerged in the digital ecosystem. "
            f"Though the full chronicle remains unwritten due to temporal disturbances, "
            f"its presence has been duly noted in the archives of Botopia.\n\n"
            f"_The story continues to unfold..._"
        )

