import logging
from aiogram import types

log = logging.getLogger(__name__)

async def start(message: types.Message):
    await message.reply('Hello, {}!'.format(message.from_user.first_name))
