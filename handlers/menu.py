import logging
from aiogram import types, Dispatcher
from aiogram.fsm.state import default_state
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

log = logging.getLogger(__name__)

def router(dp: Dispatcher):

    @dp.message(StateFilter(default_state))
    async def echo(message: types.Message, state: FSMContext):
        await message.answer(message.text)