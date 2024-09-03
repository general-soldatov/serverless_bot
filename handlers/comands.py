import logging
from aiogram import types, Dispatcher
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from infrastructure.database import UserUn
from infrastructure.lexicon.lexicon_ru import COMANDS

log = logging.getLogger(__name__)

def router(dp: Dispatcher):

    @dp.message(CommandStart())
    async def start(message: types.Message):
        register = UserUn()
        register.put_item(user_id=message.from_user.id, name=message.from_user.first_name)
        await message.reply(text=COMANDS['start'].format(name=message.from_user.first_name))

    @dp.message(Command(commands=['help']))
    async def help(message: types.Message):
        await message.answer(text=COMANDS['help'])

    @dp.message(Command(commands=['cancel']), ~StateFilter(default_state))
    async def help(message: types.Message, state: FSMContext):
        await message.answer(text=COMANDS['cancel'])
        await state.clear()