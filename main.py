import asyncio
import logging
from os import environ
from aiogram import Bot, Dispatcher, F

from __app__ import register_handlers
from infrastructure.database import YDBStorage

logger = logging.getLogger(__name__)
logger.setLevel('INFO')

async def handler():
    # Bot and dispatcher initialization
    bot = Bot(environ.get('TOKEN'))
    dp = Dispatcher(storage=YDBStorage())

    await register_handlers(dp, bot)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(handler())
