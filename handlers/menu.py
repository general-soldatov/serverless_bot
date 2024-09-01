import logging
from aiogram import types, Dispatcher

log = logging.getLogger(__name__)

# async def metodick(message: types.Message):
#     await
async def register_text(dp: Dispatcher):
    @dp.message_handler()
    async def echo(message: types.Message):
        await message.answer(message.text)