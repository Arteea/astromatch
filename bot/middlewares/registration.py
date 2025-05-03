from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from typing import Callable, Union, Dict

from services.registration.cache import RedisRegistrationCache
from services.registration.service import RegistrationService


class RegistrationMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable, event: Union[Message, CallbackQuery], data: Dict):
        '''Middleware для инициализации сервисов регистрации и кеша перед обработкой событий.
    Прокладывает в `data` экземпляры:
    - RegistrationService — для валидации, обработки и форматирования данных пользователя
    - RedisRegistrationCache — для работы с временным хранилищем данных в Redis
    Используем сервисы в каждом хендлере не создавая их каждый раз

    Args:
        handler (Callable): Обработчик события (message/callback)
        event (Union[Message, CallbackQuery]): Событие от пользователя
        data (Dict): Словарь данных контекста, куда внедряются зависимости
    '''
        user_id = event.from_user.id
        data["reg_service"] = RegistrationService(user_id=user_id)
        data["reg_cache"] = RedisRegistrationCache(user_id=user_id)    
        return await handler(event, data)