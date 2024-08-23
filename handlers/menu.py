import logging
from aiogram import types

log = logging.getLogger(__name__)

# async def metodick(message: types.Message):
#     await

async def echo(message: types.Message):
    await message.answer(message.text)