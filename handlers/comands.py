import logging
from aiogram import types, Dispatcher
from aiogram.filters import CommandStart, Command
from infrastructure.lexicon.lexicon_ru import COMANDS

log = logging.getLogger(__name__)

def router(dp: Dispatcher):

    @dp.message(CommandStart())
    async def start(message: types.Message):
        await message.reply(text=COMANDS['start'].format(name=message.from_user.first_name))

    @dp.message(Command(commands=['help']))
    async def help(message: types.Message):
        await message.answer(text=COMANDS['help'])