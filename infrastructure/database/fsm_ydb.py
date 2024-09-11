import pickle
import json
import logging

import boto3
from boto3.dynamodb.conditions import Key
from os import getenv
from dotenv import load_dotenv

from aiogram.fsm.storage.base import BaseStorage, StorageKey
from aiogram.fsm.state import State
from typing import Any, Dict, Optional

from infrastructure.configure.config import dynamodb_config

logger = logging.getLogger(__name__)

class YDBStorage(BaseStorage):
    """YDB storage for FSM"""

    def __init__(
        self,
        dynamodb=None,
        table_name: str = "fsm_storage",
    ) -> None:

        # Database
        self.dynamodb = dynamodb
        self.table_name = table_name

        if not self.dynamodb:
            load_dotenv()
            self.dynamodb = dynamodb_config


    def _create_table(self) -> None:
        """
        Create table if not exists
        """
        self.dynamodb.create_table(
            TableName = self.table_name,
            KeySchema = [
                {
                    'AttributeName': 'key',
                    'KeyType': 'HASH'  # Ключ партицирования
                }
            ],
            AttributeDefinitions = [
                {
                "AttributeName": "key",
                "AttributeType": "S"
                }
            ]
        )

    def _key(self, key: StorageKey) -> str:
        """
        Create a key for every uniqe user, chat and bot
        """
        result_string = (
            str(key.bot_id) + ":" + str(key.chat_id) + ":" + str(key.user_id)
        )
        return result_string

    def _ser(self, obj: object) -> str | bytes | None:
        """
        Serialize object
        """
        try:
            match self.serializing_method:
                case "pickle":
                    return pickle.dumps(obj)
                case "json" | _:
                    return json.dumps(obj)
        except Exception as e:
            logger.error(f"Serializing error! {e}")
            return None

    async def set_state(self, key: StorageKey, state: State | None = None) -> None:
        """
        Set state for specified key

        :param key: storage key
        :param state: new state
        """
        s_key = self._key(key)
        table = self.dynamodb.Table(self.table_name)

        try:
            table.update_item(
                Key = {
                    'key': s_key
                },
                UpdateExpression = "set state = :s ",
                ExpressionAttributeValues = {
                    ':s': state
                },
                ReturnValues = "UPDATED_NEW"
            )
        except BaseException as e:
            logger.error(f"FSM Storage set_state error: {e}")

    async def get_state(self, key: StorageKey) -> Optional[str]:
        """
        Get key state

        :param key: storage key
        :return: current state
        """
        s_key = self._key(key)
        table = self.dynamodb.Table(self.table_name)

        try:
            response = table.query(
                ProjectionExpression = 'key, state',
                KeyConditionExpression = Key('key').eq(s_key)
            )

            return response['Items'][0]['state'] if response['Items'] else None
        except KeyError:
            return
        except BaseException as e:
            logger.error(f"FSM Storage error get_state: {e}")

    async def set_data(self, key: StorageKey, data: Dict[str, Any]) -> None:
        """
        Write data (replace)

        :param key: storage key
        :param data: new data
        """
        s_key = self._key(key)
        table = self.dynamodb.Table(self.table_name)

        try:
            table.put_item(
                Item = {
                        'key': s_key,
                        'data': data
                }
            )

        except BaseException as e:
            logger.error(f"FSM Storage set_data error: {e}")

    async def get_data(self, key: StorageKey) -> Optional[Dict[str, Any]]:
        """
        Get current data for key

        :param key: storage key
        :return: current data
        """
        s_key = self._key(key)
        table = self.dynamodb.Table(self.table_name)

        try:
            response = table.query(
                ProjectionExpression = 'data',
                KeyConditionExpression = Key('key').eq(s_key)
            )

            return response['Items'][0]['data'] if response['Items'] else None

        except Exception as e:
            logger.error(f"FSM Storage error get_data: {e}")
            return None

    async def update_data(
        self, key: StorageKey, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update date in the storage for key (like dict.update)

        :param key: storage key
        :param data: partial data
        :return: new data
        """
        s_key = self._key(key)
        table = self.dynamodb.Table(self.table_name)

        try:
            table.update_item(
                Key = {
                    'key': s_key
                },
                UpdateExpression = "set data = :d ",
                ExpressionAttributeValues = {
                    ':d': data
                },
                ReturnValues = "UPDATED_NEW"
            )
        except BaseException as e:
            logger.error(f"FSM Storage update_data error: {e}")

    async def close(self) -> None:
        """
        Close storage (database connection, file or etc.)
        """

        # logger.debug("FSM Storage database has been closed.")
        self.set_data(self._key)