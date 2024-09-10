from aiogram import Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from infrastructure.database import UserVar, UserApi


def router(dp: Dispatcher):
    @dp.message(Command(commands=['task']))
    async def task(message: types.Message):
        text = UserApi().get_task()
        await message.answer(text=str(text))