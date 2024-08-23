from os import environ
from aiogram import Bot, Dispatcher

from __app__ import register_handlers

async def handler():
    # Bot and dispatcher initialization
    bot = Bot(environ.get('TOKEN'))
    dp = Dispatcher(bot)

    await register_handlers(dp)

    return {'statusCode': 200, 'body': 'ok'}
