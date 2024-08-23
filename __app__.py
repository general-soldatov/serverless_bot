import logging
from aiogram import Bot, Dispatcher, types
import handlers.comands as comand
import handlers.menu as menu

log = logging.getLogger(__name__)

# Functions for Yandex.Cloud
async def register_handlers(dp: Dispatcher):
    """Registration all handlers before processing update."""

    dp.register_message_handler(comand.start, commands=['start'])
    dp.register_message_handler(menu.echo)

    log.debug('Handlers are registered.')
