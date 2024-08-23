import logging
from aiogram import types
from infrastructure.lexicon.lexicon_ru import COMANDS

log = logging.getLogger(__name__)

async def start(message: types.Message):
    await message.reply(text=COMANDS['start'].format(name=message.from_user.first_name))

async def help(message: types.Message):
    await message.answer(text=COMANDS['help'])