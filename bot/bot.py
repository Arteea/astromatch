import asyncio
import logging
from aiogram import Bot, Dispatcher
from config_reader import config
from routers.registration import registration_router
from redis_client import storage

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher(storage=storage)

dp.include_router(registration_router)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())