import logging
from aiogram import Dispatcher
from handlers import comands, register_user, menu

log = logging.getLogger(__name__)

# Functions for Yandex.Cloud
async def register_handlers(dp: Dispatcher):
    """Registration all handlers before processing update."""
    # comands handlers
    dp.include_router(register_user.router)
    dp.include_router(comands.router)
    dp.include_router(menu.router)

    log.debug('Handlers are registered.')
