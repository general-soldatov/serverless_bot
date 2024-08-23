import logging
from aiogram import Bot, Dispatcher, types

log = logging.getLogger(__name__)
# Handlers

async def start(message: types.Message):
    await message.reply('Hello, {}!'.format(message.from_user.first_name))


async def echo(message: types.Message):
    await message.answer(message.text)


# Functions for Yandex.Cloud
async def register_handlers(dp: Dispatcher):
    """Registration all handlers before processing update."""

    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(echo)

    log.debug('Handlers are registered.')
