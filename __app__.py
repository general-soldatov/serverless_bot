import logging
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from handlers import comands, register_user, aut_user, task_solve, graph_task, admin

log = logging.getLogger(__name__)

# Functions for Yandex.Cloud
async def register_handlers(dp: Dispatcher, bot: Bot):
    """Registration all handlers before processing update."""
    # comands handlers
    comands.router(dp)
    admin.router(dp, bot)
    register_user.router(dp, bot)
    aut_user.router(dp)
    graph_task.router(dp, bot)
    task_solve.router(dp)
    # menu.router(dp)

    log.debug('Handlers are registered.')
