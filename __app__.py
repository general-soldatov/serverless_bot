import logging
from aiogram import Bot, Dispatcher, types
from handlers.comands import register_comand
from handlers.menu import register_text
from handlers.register_user import register_user

log = logging.getLogger(__name__)

# Functions for Yandex.Cloud
async def register_handlers(dp: Dispatcher):
    """Registration all handlers before processing update."""
    # comands handlers
    await register_comand(dp)
    await register_user(dp)
    # dp.register_message_handler(comand.start, commands=['start'])
    # dp.register_message_handler(comand.help, commands=['help'])

    # menu handlers

    await register_text(dp)
    # echo handlers
    # dp.register_message_handler(menu.echo)

    log.debug('Handlers are registered.')
