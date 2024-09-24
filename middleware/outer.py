import logging
from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User

from infrastructure.configure.config import bot_config, MenuConfig
from infrastructure.database import UserUn
from infrastructure.configure.lexicon import BUTTONS_RU


logger = logging.getLogger(__name__)
logger.setLevel('INFO')

class FirstOuterMiddleware(BaseMiddleware):

    @staticmethod
    def type_update(event: TelegramObject):
        data_event = event.__dict__.get('message', None)
        if not data_event:
            data_event = event.callback_query.data
            return 'callback_query', data_event
        elif data_event.text[0] == '/':
            return 'command', data_event.text
        return 'message', data_event.text

    @staticmethod
    def type_user(user: User):
        if user.id == int(bot_config.admin_ids):
            return 'admin'
        data = UserUn().info_user(user.id)[0]
        if data['active'] == 1:
            return 'junior'
        elif data['active'] == 2:
            return 'middle'
        return 'error'

    def condition(self, event, user) -> bool:
        update, content = self.type_update(event)
        type_user = self.type_user(user)
        super_condition = (type_user == 'admin' or
                           update == 'command' and content in MenuConfig().junior['commands'] or
                           update == 'callback_query' and content[:2] != 'cr')
        if super_condition:
            return True
        if update == 'message' and type_user == 'junior':
            keyboard = [BUTTONS_RU[item] for item in MenuConfig().middle['message']]
            logger.error('Message junior')
            return content not in keyboard
        if type_user == 'middle':
            if update == 'message':
                keyboard = [BUTTONS_RU[item] for item in MenuConfig().admin['message']]
                return content not in keyboard
            if update == 'command':
                return content not in MenuConfig().admin['message']

        logger.error('Outer error')

    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: Dict[str, Any]) -> Any:
        user: User = data.get('event_from_user')

        try:
            if user is None:
                return

            if self.condition(event, user):
                result = await handler(event, data)
                return result
        except IndexError:
            user_id = user.id
            name = f'{user.first_name} {user.last_name}'
            UserUn().put_item(user_id, name)
            logger.error(f'Add user {user_id} {user.first_name} {user.last_name}')
        except Exception as e:
            logger.error(f'Middleware {user.id} {e}')
