from redis_client import redis_client as r

from logger.logger_config import get_logger

logger = get_logger(__name__)

class RedisRegistrationCache:
    
    def __init__(self, user_id):
        self.user_key = f"{user_id}"
    
    async def set_value(self, key, value, seconds=3600):
        await r.hset(self.user_key, mapping={key: value})
        await r.expire(key, seconds)
    
    async def get_all_info_from_cache(self):
        info = await r.hgetall(self.user_key)
        return info
    
    async def get_value(self, key):
        value = await r.hget(self.user_key, key)
        return value
    
    @property
    def media_key(self):
        return f"{self.user_key}:media"
    
    async def add_media(self, file_id: str, seconds=3600):
        await r.sadd(self.media_key, file_id)
        file = await self.get_all_users_media_from_cache()     
        await r.expire(self.media_key, seconds)
    
    async def get_all_users_media_from_cache(self):
        result = await r.smembers(self.media_key)
        return result