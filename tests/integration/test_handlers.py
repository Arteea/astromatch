import pytest
from bot.routers.registration import cmd_start,handle_contact
from bot.utils.keyboards import RegistrationKeyboards as r
from unittest.mock import AsyncMock,Mock, MagicMock
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from tests.test_data.handlers_data import HandlersData as h
from bot.services.registration.service import RegistrationService
from bot.services.registration.cache import RedisRegistrationCache


@pytest.mark.parametrize("user",h.start_handler_data)
@pytest.mark.asyncio
async def test_start_handler(user):
    mock_message = AsyncMock()
    mock_message.from_user = user
    await cmd_start(mock_message)

    keyboard = r.contact_step_keyboard
    mock_message.answer.assert_called_with(f"Привет, {mock_message.from_user.full_name} Я астрологический дейтинг бот!\n"
                                           "Создан для того,чтобы найти тебе пару исходя из твоего знака зодиака.\n"
                                           "Чтобы начать получать предложения для знакомства нужно зарегистрироваться.",reply_markup=keyboard)


@pytest.mark.parametrize("user, contact, user_chat, expected_state, expected_message, expected_phone",
                         h.contact_handler_data)
@pytest.mark.asyncio
async def test_handle_contact(redis_storage, mocked_bot, user, contact,
                            user_chat, expected_state, expected_message, expected_phone):
    
    mock_message = AsyncMock()
    mock_message.from_user = user
    mock_message.contact = contact

    state = FSMContext(
        storage=redis_storage,
        key=StorageKey(bot_id=mocked_bot.id, user_id=user.id,
                       chat_id=user_chat.id)
    )

    reg_service = RegistrationService(user_id=user.id)
    reg_cache = RedisRegistrationCache(user_id=user.id,
                                       redis=redis_storage.redis)

    await handle_contact(message=mock_message, state=state,
                         reg_service=reg_service,
                         reg_cache=reg_cache)
    
    assert await state.get_state() == expected_state
    mock_message.answer.assert_called_with(expected_message)
    assert await reg_cache.get_value("phone") == expected_phone



