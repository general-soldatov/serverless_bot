import asyncio
from os import environ
from aiogram import Bot, Dispatcher, F
from aiogram.fsm.storage.memory import MemoryStorage


from __app__ import register_handlers
from infrastructure.fsm_ydb import YDBStorage


async def handler():
    # Bot and dispatcher initialization
    bot = Bot(environ.get('TOKEN'))
    dp = Dispatcher(storage=YDBStorage())

    await register_handlers(dp)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(handler())
