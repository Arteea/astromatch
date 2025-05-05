from aiogram import Dispatcher
import pytest
import pytest_asyncio
from _pytest.config import UsageError
from aiogram.fsm.storage.redis import RedisStorage
from tests.mocked_bot import MockedBot
from redis.asyncio.connection import parse_url as parse_redis_url
from redis.exceptions import ConnectionError
import asyncio
import sys


SKIP_MESSAGE_PATTERN = 'Need "--{db}" option with {db} URI to run'
INVALID_URI_PATTERN = "Invalid {db} URI {uri!r}: {err}"


def pytest_addoption(parser):
    parser.addoption("--redis", default=None, help="run tests which require redis connection")


def pytest_configure(config):
    config.addinivalue_line("markers", "redis: marked tests require redis connection to run")

    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    else:
        asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())



@pytest.fixture(scope="function")
def redis_server(request):
    redis_uri = request.config.getoption("--redis")
    if redis_uri is None:
        pytest.skip(SKIP_MESSAGE_PATTERN.format(db="redis"))
    else:
        return redis_uri


@pytest_asyncio.fixture(scope="function")
async def redis_storage(redis_server):
    try:
        parse_redis_url(redis_server)
    except ValueError as e:
        raise UsageError(INVALID_URI_PATTERN.format(db="redis", uri=redis_server, err=e))
    storage = RedisStorage.from_url(redis_server)
    try:
        await storage.redis.info()
    except ConnectionError as e:
        pytest.fail(str(e))
    try:
        yield storage
    finally:
        conn = await storage.redis
        await conn.flushdb()
        await storage.close()


@pytest.fixture(scope="function")
def mocked_bot():
    return MockedBot()


@pytest_asyncio.fixture()
async def dispatcher():
    dp = Dispatcher()
    await dp.emit_startup()
    try:
        yield dp
    finally:
        await dp.emit_shutdown()

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

