import logging
from aiogram import types, Dispatcher

log = logging.getLogger(__name__)

def router(dp: Dispatcher):

    @dp.message()
    async def echo(message: types.Message):
        await message.answer(message.text)