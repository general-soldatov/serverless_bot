import logging
from aiogram import types, Dispatcher
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from infrastructure.buttons import UserButton
from infrastructure.database import UserUn
from infrastructure.lexicon.lexicon_ru import COMANDS

log = logging.getLogger(__name__)

def router(dp: Dispatcher):

    @dp.message(CommandStart())
    async def start(message: types.Message):
        register = UserUn()
        register.put_item(user_id=message.from_user.id, name=message.from_user.first_name)
        buttons = UserButton().unauth_user()
        await message.reply(text=COMANDS['start'].format(name=message.from_user.first_name),
                            reply_markup=buttons)

    @dp.message(Command(commands=['help']))
    async def help(message: types.Message):
        await message.answer(text=COMANDS['help'])

    @dp.message(Command(commands=['menu']))
    async def help(message: types.Message):
        buttons = UserButton()(user_id=message.from_user.id)
        await message.answer(text=COMANDS['menu'], reply_markup=buttons)

    @dp.message(Command(commands=['cancel']), StateFilter(default_state))
    async def help(message: types.Message):
        await message.answer(text=COMANDS['cancel_not'])

    @dp.message(Command(commands=['cancel']), ~StateFilter(default_state))
    async def help(message: types.Message, state: FSMContext):
        await message.answer(text=COMANDS['cancel'])
        await state.clear()