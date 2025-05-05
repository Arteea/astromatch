from redis_client import redis_client as r

from logger.logger_config import get_logger

logger = get_logger(__name__)

class RedisRegistrationCache:
    '''
    Класс для работы с кэшем регистрации пользователя в Redis.
    Сохраняет и извлекает данные пользователя, включая основную информацию 
    и загруженные медиафайлы, с использованием Redis Hash и Set структур.
    Атрибуты:
        user_key (str): Ключ Redis, уникальный для каждого пользователя.
    '''
    def __init__(self, user_id, redis=r):
        self.user_key = f"{user_id}"
        self.redis = redis
    async def set_value(self, key, value, seconds=3600):
        '''
        Устанавливает значение в Redis Hash для текущего пользователя.
        Args:
            key (str): Ключ внутри хэша пользователя.
            value (str): Значение, связанное с ключом.
            seconds (int, optional): Время жизни ключа в секундах. По умолчанию 3600.
        '''
        await self.redis.hset(self.user_key, mapping={key: value})
        await self.redis.expire(key, seconds)
    
    async def get_all_info_from_cache(self):
        '''Получает всю сохраненную информацию пользователя из Redis Hash.
        Returns:
            dict: Все пары ключ-значение, сохраненные в хэше пользователя за время регистрации.'''
        info = await self.redis.hgetall(self.user_key)
        return info
    
    async def get_value(self, key):
        '''Получает значение из Redis Hash текущего пользователя по ключу.
        Args:
            key (str): Ключ для получения значения.
        Returns:
            str or None:'''
        value = await self.redis.hget(self.user_key, key)
        return value
    
    @property
    def media_key(self):
        '''
        Генерирует ключ Redis для хранения медиафайлов пользователя до окончания регистрации'''
        return f"{self.user_key}:media"
    
    async def add_media(self, file_id: str, seconds=3600):
        '''
        Добавляет идентификатор медиафайла в Redis Set и обновляет TTL.
        Args:
            file_id (str): Идентификатор медиафайла file_id из Telegram.
            seconds (int, optional): Время жизни ключа в секундах. По умолчанию 3600.
        '''
        await self.redis.sadd(self.media_key, file_id)  
        await self.redis.expire(self.media_key, seconds)
    
    async def get_all_users_media_from_cache(self):
        """
        Получает все медиафайлы текущего пользователя из Redis Set.
        Returns:
            set: Множество идентификаторов медиа file_id.
        """
        result = await self.redis.smembers(self.media_key)
        return result