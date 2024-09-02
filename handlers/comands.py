import logging
from aiogram import types, Router
from aiogram.filters import CommandStart, Command
from infrastructure.lexicon.lexicon_ru import COMANDS

log = logging.getLogger(__name__)

router = Router()

@router.message(CommandStart())
async def start(message: types.Message):
    await message.reply(text=COMANDS['start'].format(name=message.from_user.first_name))

@router.message(Command(commands=['help']))
async def help(message: types.Message):
    await message.answer(text=COMANDS['help'])