import logging
from aiogram import types, Router

log = logging.getLogger(__name__)

router = Router()

@router.message()
async def echo(message: types.Message):
    await message.answer(message.text)