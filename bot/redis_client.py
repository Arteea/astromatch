from redis.asyncio import Redis
from aiogram.fsm.storage.redis import RedisStorage

redis_client = Redis(host="localhost",port=6379, db=0, decode_responses=True)
storage = RedisStorage(redis=redis_client)
