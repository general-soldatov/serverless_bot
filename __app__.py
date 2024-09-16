import logging
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from handlers import comands, register_user, aut_user, task_solve, graph_task, admin
from middleware.outer import FirstOuterMiddleware

logger = logging.getLogger(__name__)
logger.setLevel('INFO')

# Functions for Yandex.Cloud
async def register_handlers(dp: Dispatcher, bot: Bot):
    """Registration all handlers before processing update."""
    # comands handlers
    dp.update.middleware(FirstOuterMiddleware())
    comands.router(dp)
    register_user.router(dp, bot)
    aut_user.router(dp, bot)
    graph_task.router(dp, bot)
    task_solve.router(dp)

    # dp.update.middleware(AdminMiddleware())
    admin.router(dp, bot)
    # menu.router(dp)

    logger.debug('Handlers are registered.')
