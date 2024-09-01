import asyncio
from os import environ
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from __app__ import register_handlers

async def handler():
    # Bot and dispatcher initialization
    bot = Bot(environ.get('TOKEN'))
    dp = Dispatcher(bot, storage=MemoryStorage())

    await register_handlers(dp)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(handler())
