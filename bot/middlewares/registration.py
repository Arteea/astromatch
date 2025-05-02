from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from typing import Callable, Union, Dict

from services.registration.cache import RedisRegistrationCache
from services.registration.service import RegistrationService


class RegistrationMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable, event: Union[Message, CallbackQuery], data: Dict):
        user_id = event.from_user.id
        data["reg_service"] = RegistrationService(user_id=user_id)
        data["reg_cache"] = RedisRegistrationCache(user_id=user_id)    
        return await handler(event, data)