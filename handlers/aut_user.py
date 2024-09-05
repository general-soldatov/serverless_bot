import logging
from aiogram import types, Dispatcher, F

from infrastructure.lexicon.buttons import BUTTONS_RU

log = logging.getLogger(__name__)

def router(dp: Dispatcher):

    @dp.message(F.text == BUTTONS_RU['profile'])
    async def echo(message: types.Message):

        await message.answer(message.text)