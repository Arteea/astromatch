from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, Contact, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters.command import Command
from aiogram.filters import StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from redis_client import redis_client as r
from utils.zodiac_buttons import zodiac_keyboard
from services.registration.service import RegistrationService
from services.registration.cache import RedisRegistrationCache
from middlewares.registration import RegistrationMiddleware
from aiogram.utils.media_group import MediaGroupBuilder

from logger.logger_config import get_logger

logger = get_logger(__name__)



registration_router = Router()
registration_middleware = RegistrationMiddleware()

registration_router.message.middleware(registration_middleware)
registration_router.callback_query.middleware(registration_middleware)

class RegistrationForm(StatesGroup):
    
    phone = State()
    name = State()
    gender = State()
    age = State()
    zodiac = State()
    description = State()
    city = State()
    media = State()
    conclusion = State()



@registration_router.message(Command("start"))
async def cmd_start(message: Message):
    kb = [[KeyboardButton(text="Телефон",request_contact=True)]]  
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True,
                                  one_time_keyboard=True, 
                                  input_field_placeholder="Отправьте свой контакт для регистрации:")
    await message.answer(f"Привет, {message.from_user.full_name} Я астрологический дейтинг бот!\nСоздан для того,чтобы найти тебе пару исходя из твоего знака зодиака.\nЧтобы начать получать предложения для знакомства нужно зарегистрироваться.",reply_markup=keyboard)



@registration_router.message(F.contact)
async def handle_contact(message: Message, state: FSMContext,
                        reg_service: RegistrationService,
                        reg_cache: RedisRegistrationCache):
    if message.contact.user_id != message.from_user.id:
        await message.answer("Пожалуйста, отправьте именно свой номер через кнопку, не пересылайте чужой контакт 🙏")
        return             
    try:
        phone_number = reg_service.set_phone(message.contact.phone_number)
        await reg_cache.set_value("phone", phone_number)
        await state.set_state(RegistrationForm.name)
        await message.answer("Введите ваше имя(именно так вас будут видеть другие пользователи):")
    except Exception as e:
        await message.answer(f"{e}")
        return


@registration_router.message(RegistrationForm.name)
async def handle_username(message: Message, state: FSMContext,
                     reg_service: RegistrationService,
                     reg_cache: RedisRegistrationCache):
    try:
        username = reg_service.set_username(message.text)
        logger.info(f"ИМЯ пользователя {username}")
        await reg_cache.set_value("username", username)
        await state.set_state(RegistrationForm.gender)
        kb = [[InlineKeyboardButton(text="Мужской",callback_data="gender:male"),
            InlineKeyboardButton(text="Женский", callback_data="gender:female")]]
        keyboard = InlineKeyboardMarkup(inline_keyboard=kb,
                                        resize_keyboard=True,
                                        one_time_keyboard=True, 
                                        input_field_placeholder="Ваш пол:")
        await message.answer(f"Выберите ваш пол:", reply_markup=keyboard)
    except Exception as e:
        await message.answer(f"{e}")
        return

@registration_router.callback_query(F.data.startswith('gender:'))
async def handle_gender(data: CallbackQuery, state: FSMContext,
                        reg_service: RegistrationService,
                        reg_cache: RedisRegistrationCache):
    try:
        sex = data.data.split(':')[1]
        gender = reg_service.set_gender(sex)
        await reg_cache.set_value("gender", gender)
        await state.set_state(RegistrationForm.age)
        await data.message.answer("Отлично! Теперь введите сколько Вам лет:")
        await data.answer()
    except Exception as e:
        await data.message.answer(f"{e}")
        await data.answer()
        return


@registration_router.message(RegistrationForm.age)
async def handle_age(message: Message, state: FSMContext,
                        reg_service: RegistrationService,
                        reg_cache: RedisRegistrationCache):
    try:
        age = reg_service.set_age(message.text)
        await reg_cache.set_value("age", age)
        await state.set_state(RegistrationForm.zodiac)
        await message.answer("Выберите свой знак зодиака:", reply_markup=zodiac_keyboard)
    except Exception as e:
        await message.answer(f"{e}")
        return


@registration_router.callback_query(F.data.startswith('zodiac:'))
async def handle_zodiac(data: CallbackQuery, state: FSMContext,
                        reg_service: RegistrationService,
                        reg_cache: RedisRegistrationCache):
    try:
        zodiac_sign = data.data.split(':')[1]
        reg_service.set_zodiac(zodiac_sign)
        await reg_cache.set_value('zodiac_sign',zodiac_sign)
        await state.set_state(RegistrationForm.description)
        await data.message.answer(f"Дополните описание о себе")
        await data.answer()
    except Exception as e:
        print(f"{e}")
        return


@registration_router.message(RegistrationForm.description)
async def handle_description(message: Message, state: FSMContext,
                            reg_service: RegistrationService,
                            reg_cache: RedisRegistrationCache):
    try:
        description = reg_service.set_description(message.text)
        await reg_cache.set_value('description', description)
        kb = [[KeyboardButton(text="Местоположение", request_location=True)]]  
        keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True,
                                  one_time_keyboard=True, 
                                  input_field_placeholder="Отправьте свое местоположение, чтобы подобрать пару рядом с вами")
        await state.set_state(RegistrationForm.city)
        await message.answer("Поделитесь геопозицией через кнопку,либо отправьте сообщение с Вашим городом", reply_markup=keyboard)
    except Exception as e:
        await message.answer(f"{e}")
        return
    

@registration_router.message(RegistrationForm.city)
async def handle_city(message: Message, state: FSMContext,
                    reg_service: RegistrationService,
                    reg_cache: RedisRegistrationCache):
    try:
        location = message.location
        if location:
            lat,lon = location.latitude, location.longitude
            city, region = await reg_service.set_city(lat=lat, lon=lon)
        elif message.text:
            city, region = await reg_service.set_city(city=message.text)
        await reg_cache.set_value("city", city)
        await reg_cache.set_value("region", region)
        await state.set_state(RegistrationForm.media)
        await message.answer(f"И последний шаг - добавление фотографии,можешь загрузить до 5 медиафайлов")
    except Exception as e:
        await message.answer(f"{e}")
        return
    

MAX_MEDIA_COUNT = 5

@registration_router.message(StateFilter(RegistrationForm.media),
                             F.content_type.in_({"photo", "video"}))
async def handle_media(message: Message, state: FSMContext,
                    reg_service: RegistrationService,
                    reg_cache: RedisRegistrationCache):
    try:
        set_of_users_media = await reg_cache.get_all_users_media_from_cache()
        logger.info(f'Начался шаг с медиа')
        logger.info(f'Всего медиафайлов{set_of_users_media}')
        if len(set_of_users_media) >= MAX_MEDIA_COUNT:
            await message.answer(f"Получено 5 файлов. Переходим к следующему шагу.")
            await state.set_state(RegistrationForm.conclusion)
            return
        else:
            file_id = await reg_service.get_media_id_from_message(message)
            await reg_cache.add_media(file_id)
            finish_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="✅ Завершить загрузку", callback_data="finish_media_upload")]])
            # await message.answer("Файл принят. Когда закончите загрузку всех файлов, нажмите кнопку ниже.",
            #          reply_markup=finish_kb)
            await message.answer(
            f"Файл принят ({len(set_of_users_media)}/{MAX_MEDIA_COUNT}). "
            "Можете продолжить загрузку до 5 файлов или нажмите кнопку, если закончили.",
            reply_markup=finish_kb)
    except Exception as e:
        await message.answer(f"{e}")
        return

@registration_router.message(StateFilter(RegistrationForm.media),
                             F.content_type.in_({"text", "document", "audio", "voice", "sticker", "animation", "location"}))
async def handle_media_error(message: Message):
    await message.answer("Пришлите фото или видео для анкеты")
    return


@registration_router.callback_query(F.data == "finish_media_upload")
async def redirect_conclusion(data: CallbackQuery, state: FSMContext):
    await state.set_state(RegistrationForm.conclusion)
    await data.message.answer("📨 Хочешь посмотреть как будет выглядеть твоя анкета?")
    await data.answer()
    return
    


@registration_router.message(StateFilter(RegistrationForm.conclusion))
async def handle_conclusion(message: Message, state: FSMContext,
                        reg_service: RegistrationService,
                        reg_cache: RedisRegistrationCache):
    logger.info(f"ТЕПЕРЬ ЗАКЛЮЧИТЕЛЬНЫЙ ШАГ")
    info = await reg_cache.get_all_info_from_cache()
    media = await reg_cache.get_all_users_media_from_cache()
    media_group = await reg_service.collect_media_in_mediagroup(media)
    caption = reg_service.format_user_info(info)
    media_group.caption = caption
    await message.answer_media_group(media=media_group.build())
    return