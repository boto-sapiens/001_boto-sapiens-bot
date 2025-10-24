"""User interaction handlers."""
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from loguru import logger

from services.api_repository import ApiUserRepository, ApiBotRepository
from bot.dependencies import get_symfony_api, get_bot
from services.telegram_publisher import TelegramPublisher
from services.openai_service import OpenAIService
from bot.config import settings


router = Router()


class RegistrationStates(StatesGroup):
    """States for user registration process."""
    waiting_for_bio = State()
    waiting_for_interests = State()


class BotRegistrationStates(StatesGroup):
    """States for bot registration process."""
    waiting_for_bot_name = State()
    waiting_for_bot_username = State()
    waiting_for_bot_description = State()
    waiting_for_bot_purpose = State()
    waiting_for_publish_confirmation = State()


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    """Handle /start command."""
    user = await ApiUserRepository.get_by_telegram_id(message.from_user.id)
    symfony_api = get_symfony_api()
    
    if user:
        # Sync existing user with Symfony API
        if symfony_api:
            try:
                await symfony_api.upsert_user(
                    telegram_id=str(message.from_user.id),
                    username=message.from_user.username
                )
            except Exception as e:
                logger.warning(f"Failed to sync user with Symfony API: {e}")
        
        await message.answer(
            f"👋 С возвращением, {user.full_name}!\n\n"
            "Доступные команды:\n"
            "/profile - Обновить профиль\n"
            "/add_bot - Добавить нового бота\n"
            "/my_bots - Посмотреть мои боты\n"
            "/help - Помощь"
        )
    else:
        # Create new user via API
        await ApiUserRepository.create(
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            full_name=message.from_user.full_name or "Пользователь"
        )
        
        # Sync new user with Symfony API
        if symfony_api:
            try:
                result = await symfony_api.upsert_user(
                    telegram_id=str(message.from_user.id),
                    username=message.from_user.username
                )
                if result.get("status") != "success":
                    logger.warning(f"Symfony API returned non-success status: {result}")
            except Exception as e:
                logger.warning(f"Failed to sync new user with Symfony API: {e}")
        
        await message.answer(
            "👋 Привет! Я boto-sapiens - бот для изучения экосистемы Telegram ботов.\n\n"
            "🧬 Я собираю информацию о вас и ваших ботах, чтобы создавать ежедневные отчеты "
            "о состоянии нашей 'цифровой экосистемы'.\n\n"
            "Давайте начнём! Расскажите немного о себе:\n"
            "/profile - Заполнить профиль\n"
            "/add_bot - Добавить информацию о вашем боте"
        )


@router.message(Command("profile"))
async def cmd_profile(message: Message, state: FSMContext) -> None:
    """Start profile update."""
    await message.answer(
        "📝 Давайте обновим ваш профиль!\n\n"
        "Расскажите о себе (bio). Кто вы, чем занимаетесь?"
    )
    await state.set_state(RegistrationStates.waiting_for_bio)


@router.message(RegistrationStates.waiting_for_bio)
async def process_bio(message: Message, state: FSMContext) -> None:
    """Process user bio."""
    await state.update_data(bio=message.text)
    await message.answer(
        "👍 Отлично!\n\n"
        "Теперь расскажите о ваших интересах. Что вас интересует в мире ботов и технологий?"
    )
    await state.set_state(RegistrationStates.waiting_for_interests)


@router.message(RegistrationStates.waiting_for_interests)
async def process_interests(message: Message, state: FSMContext) -> None:
    """Process user interests."""
    data = await state.get_data()
    bio = data.get("bio")
    
    await ApiUserRepository.update_profile(
        telegram_id=message.from_user.id,
        bio=bio,
        interests=message.text
    )
    
    await message.answer(
        "✅ Профиль обновлён!\n\n"
        "Теперь вы можете добавить информацию о ваших ботах:\n"
        "/add_bot - Добавить бота"
    )
    await state.clear()


@router.message(Command("add_bot"))
async def cmd_add_bot(message: Message, state: FSMContext) -> None:
    """Start bot registration."""
    await message.answer(
        "🤖 Давайте добавим информацию о вашем боте!\n\n"
        "Как называется ваш бот?"
    )
    await state.set_state(BotRegistrationStates.waiting_for_bot_name)


@router.message(BotRegistrationStates.waiting_for_bot_name)
async def process_bot_name(message: Message, state: FSMContext) -> None:
    """Process bot name."""
    await state.update_data(bot_name=message.text)
    await message.answer(
        "👍 Отлично!\n\n"
        "Какой username у вашего бота? (например: @mybot или пропустите, отправив /skip)"
    )
    await state.set_state(BotRegistrationStates.waiting_for_bot_username)


@router.message(BotRegistrationStates.waiting_for_bot_username)
async def process_bot_username(message: Message, state: FSMContext) -> None:
    """Process bot username."""
    username = None if message.text == "/skip" else message.text
    await state.update_data(bot_username=username)
    await message.answer(
        "Опишите вашего бота. Что он делает?"
    )
    await state.set_state(BotRegistrationStates.waiting_for_bot_description)


@router.message(BotRegistrationStates.waiting_for_bot_description)
async def process_bot_description(message: Message, state: FSMContext) -> None:
    """Process bot description."""
    await state.update_data(bot_description=message.text)
    await message.answer(
        "И последний вопрос: какова цель вашего бота? Для чего вы его создали?"
    )
    await state.set_state(BotRegistrationStates.waiting_for_bot_purpose)


@router.message(BotRegistrationStates.waiting_for_bot_purpose)
async def process_bot_purpose(message: Message, state: FSMContext) -> None:
    """Process bot purpose and save."""
    # Get data and immediately change state to prevent double processing
    data = await state.get_data()
    
    # Change state immediately to prevent duplicate processing
    await state.set_state(BotRegistrationStates.waiting_for_publish_confirmation)
    
    symfony_api = get_symfony_api()
    
    # Save bot via API
    bot_record = await ApiBotRepository.create(
        owner_telegram_id=message.from_user.id,
        bot_name=data["bot_name"],
        bot_username=data.get("bot_username"),
        bot_description=data["bot_description"],
        bot_purpose=message.text
    )
    
    # Sync bot with Symfony API
    if symfony_api and data.get("bot_username"):
        try:
            result = await symfony_api.add_bot(
                telegram_id=str(message.from_user.id),
                bot_username=data["bot_username"],
                description=data["bot_description"]
            )
            if result.get("status") != "success":
                logger.warning(f"Symfony API returned non-success status for bot: {result}")
        except Exception as e:
            logger.warning(f"Failed to sync bot with Symfony API: {e}")
    
    # Store complete bot data in state for callback handlers
    await state.update_data(
        bot_id=bot_record.get('id') if bot_record else None,
        bot_purpose=message.text,
        creator_name=message.from_user.full_name or message.from_user.username or "Anonymous"
    )
    
    # Show confirmation dialog for chronicle publishing
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Yes", callback_data=f"publish_yes:{bot_record.get('id') if bot_record else 'unknown'}"),
            InlineKeyboardButton(text="❌ No", callback_data=f"publish_no:{bot_record.get('id') if bot_record else 'unknown'}")
        ]
    ])
    
    await message.answer(
        "✅ Bot successfully added!\n\n"
        "A new species has been registered.\n"
        "Do you want to publish its Chronicle to the Boto Sapiens channel?",
        reply_markup=keyboard
    )


@router.callback_query(F.data.startswith("publish_yes:"))
async def process_publish_confirmed(callback: CallbackQuery, state: FSMContext) -> None:
    """Handle user confirmation to publish chronicle."""
    # Get bot data from state
    data = await state.get_data()
    bot_instance = get_bot()
    
    # Log decision
    logger.info(f"User {callback.from_user.id} chose to publish chronicle for bot: {data.get('bot_name')}")
    
    # Answer callback to remove loading state
    await callback.answer()
    
    # Edit message to show generation in progress
    await callback.message.edit_text(
        "✅ Bot successfully added!\n\n"
        "🔮 Generating chronicle... The Chronicler is observing the new species..."
    )
    
    try:
        # Generate chronicle via OpenAI
        openai_service = OpenAIService()
        chronicle = await openai_service.generate_single_species_chronicle(
            bot_name=data.get("bot_name"),
            bot_username=data.get("bot_username"),
            description=data.get("bot_description"),
            purpose=data.get("bot_purpose")
        )
        
        # Publish to channel if configured
        if bot_instance and settings.telegram_channel_id:
            publisher = TelegramPublisher(bot_instance)
            success = await publisher.post_species_report(chronicle)
            
            if success:
                await callback.message.edit_text(
                    "✅ Bot successfully added!\n\n"
                    "📜 The Chronicle has been written and published to the archives.\n\n"
                    "You can add more bots: /add_bot\n"
                    "Or view your bots: /my_bots"
                )
            else:
                await callback.message.edit_text(
                    "✅ Bot successfully added!\n\n"
                    "📜 Chronicle was generated but could not be published to the channel.\n"
                    "The bot is saved in the database.\n\n"
                    "You can add more bots: /add_bot\n"
                    "Or view your bots: /my_bots"
                )
        else:
            await callback.message.edit_text(
                "✅ Bot successfully added!\n\n"
                "📜 Chronicle generated, but channel is not configured.\n\n"
                "You can add more bots: /add_bot\n"
                "Or view your bots: /my_bots"
            )
            
    except Exception as e:
        logger.error(f"Failed to generate or publish chronicle: {e}")
        await callback.message.edit_text(
            "✅ Bot successfully added!\n\n"
            "⚠️ There was an issue generating the chronicle, but your bot is safely recorded.\n\n"
            "You can add more bots: /add_bot\n"
            "Or view your bots: /my_bots"
        )
    
    # Clear state
    await state.clear()


@router.callback_query(F.data.startswith("publish_no:"))
async def process_publish_declined(callback: CallbackQuery, state: FSMContext) -> None:
    """Handle user declining to publish chronicle."""
    # Get bot data from state
    data = await state.get_data()
    
    # Log decision
    logger.info(f"User {callback.from_user.id} declined to publish chronicle for bot: {data.get('bot_name')}")
    
    # Answer callback to remove loading state
    await callback.answer()
    
    # Edit message
    await callback.message.edit_text(
        "✅ Bot successfully added!\n\n"
        "Alright. The Chronicle will remain in the archives for now.\n\n"
        "You can add more bots: /add_bot\n"
        "Or view your bots: /my_bots"
    )
    
    # Clear state
    await state.clear()


@router.message(Command("my_bots"))
async def cmd_my_bots(message: Message) -> None:
    """Show user's bots."""
    bots = await ApiBotRepository.get_by_owner(message.from_user.id)
    
    if not bots:
        await message.answer(
            "У вас пока нет добавленных ботов.\n\n"
            "Добавьте первого: /add_bot"
        )
        return
    
    response = "🤖 Ваши боты:\n\n"
    for i, bot in enumerate(bots, 1):
        response += f"{i}. {bot.get('bot_name', 'Unknown')}"
        if bot.get('bot_username'):
            response += f" ({bot['bot_username']})"
        response += f"\n   📝 {bot.get('bot_description', 'No description')}\n"
        response += f"   🎯 Цель: {bot.get('bot_purpose', 'No purpose specified')}\n\n"
    
    await message.answer(response)


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    """Show help message."""
    await message.answer(
        "🧬 boto-sapiens - Изучаем экосистему Telegram ботов\n\n"
        "📋 Доступные команды:\n\n"
        "/start - Начать работу\n"
        "/profile - Обновить профиль\n"
        "/add_bot - Добавить бота\n"
        "/my_bots - Мои боты\n"
        "/help - Эта справка\n\n"
        "💡 Каждый день я генерирую Species Report - отчёт о состоянии "
        "нашей экосистемы ботов с использованием AI!"
    )

