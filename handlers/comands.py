import logging
from aiogram import types, Dispatcher
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from infrastructure.keyboard import UserButton
from infrastructure.database import UserUn
from infrastructure.configure.lexicon import COMMANDS

log = logging.getLogger(__name__)

def router(dp: Dispatcher):

    @dp.message(CommandStart())
    async def start(message: types.Message):
        register = UserUn()
        register.put_item(user_id=message.from_user.id, name=message.from_user.first_name)
        buttons = UserButton().unauth_user()
        await message.reply(text=COMMANDS['start'].format(name=message.from_user.first_name),
                            reply_markup=buttons)

    @dp.message(Command(commands=['help']))
    async def help(message: types.Message):
        await message.answer(text=COMMANDS['help'])

    @dp.message(Command(commands=['menu']))
    async def menu(message: types.Message):
        buttons = UserButton(width=3)(user_id=message.from_user.id)
        await message.answer(text=COMMANDS['menu'], reply_markup=buttons)

    @dp.message(Command(commands=['cancel']), StateFilter(default_state))
    async def cancel(message: types.Message):
        await message.answer(text=COMMANDS['cancel_not'])

    @dp.message(Command(commands=['cancel']), ~StateFilter(default_state))
    async def cancel_state(message: types.Message, state: FSMContext):
        await message.answer(text=COMMANDS['cancel'])
        await state.clear()
