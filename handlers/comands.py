import logging
from aiogram import types, Dispatcher
from infrastructure.lexicon.lexicon_ru import COMANDS

log = logging.getLogger(__name__)

async def register_comand(dp: Dispatcher):
    @dp.message_handler(commands=['start'])
    async def start(message: types.Message):
        await message.reply(text=COMANDS['start'].format(name=message.from_user.first_name))

    @dp.message_handler(commands=['help'])
    async def help(message: types.Message):
        await message.answer(text=COMANDS['help'])