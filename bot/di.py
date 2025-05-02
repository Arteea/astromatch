from services.registration.cache import RedisRegistrationCache
from services.registration.service import RegistrationService
from aiogram.types import Message

async def get_registration_cache(message: Message) -> RedisRegistrationCache:
    return RedisRegistrationCache(user_id=message.from_user.id)

async def get_registration_service(message: Message) -> RegistrationService:
    return RegistrationService(user_id=message.from_user.id)