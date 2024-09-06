import logging
from aiogram import Dispatcher
from dotenv import load_dotenv
from handlers import comands, register_user, aut_user

log = logging.getLogger(__name__)

# Functions for Yandex.Cloud
async def register_handlers(dp: Dispatcher):
    """Registration all handlers before processing update."""
    # comands handlers
    comands.router(dp)
    register_user.router(dp)
    aut_user.router(dp)
    # menu.router(dp)

    log.debug('Handlers are registered.')
