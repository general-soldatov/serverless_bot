import json
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.types import update
from __app__ import register_handlers
from infrastructure.database import YDBStorage


# Logger initialization and logging level setting
log = logging.getLogger(__name__)
log.setLevel('INFO')


async def process_event(event, dp: Dispatcher, bot: Bot):
    """
    Converting an Yandex.Cloud functions event to an update and
    handling tha update.
    """
    up: dict = json.loads(event['body'])

    my_update = update.Update.model_validate(up, context={"bot": bot})
    await dp.feed_update(bot, my_update)


async def handler(event, context):
    """Yandex.Cloud functions handler."""

    if event['httpMethod'] == 'POST':
        # Bot and dispatcher initialization
        bot = Bot(os.environ.get('TOKEN'))
        dp = Dispatcher(storage=YDBStorage())

        await register_handlers(dp, bot)
        await process_event(event, dp, bot)

        return {'statusCode': 200, 'body': 'ok'}
    return {'statusCode': 405}
