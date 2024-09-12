import boto3
from boto3.dynamodb.conditions import Key
from os import getenv
from dotenv import load_dotenv

from infrastructure.configure.config import dynamodb_config

class UserUn:
    """Класс для управления записями в базе данных YDB, название класса не принципиально.
    """
    def __init__(self, dynamodb=None):
        """Инициализация базы данных и сервисного аккаунта, в целях безопасности используются
           переменные окружения, либо указанные в файле .env
        """
        self.dynamodb = dynamodb
        self.table = 'User_Unauthorized'
        if not self.dynamodb:
            load_dotenv()
            self.dynamodb = dynamodb_config

    def create_table(self):
        """Метод создания таблицы, инициализируются ключи и столбцы таблицы
        """
        table = self.dynamodb.create_table(
            TableName = self.table,
            KeySchema = [
                {
                    'AttributeName': 'user_id',
                    'KeyType': 'HASH'  # Ключ партицирования, можно добавить дополнительно ключ сортировки Range
                }
            ],
            AttributeDefinitions = [
                {
                "AttributeName": "user_id",
                "AttributeType": "N"
                },
                {
                "AttributeName": "name",
                "AttributeType": "S"
                },
                {
                "AttributeName": "active",
                "AttributeType": "N"
                }
            ]
        )
        return table

    def put_item(self, user_id, name, active=1):
        """Метод добавления записи в таблицу.
        """
        table = self.dynamodb.Table(self.table)
        response = table.put_item(
            Item = {
                    'user_id': user_id,
                    'name': name,
                    'active': active,
            }
        )
        return response

    def update_active(self, user_id, active):
        """Метод смены активности в случае блокировки бота пользователем.
        """
        table = self.dynamodb.Table(self.table)
        response = table.update_item(
            Key = {
                'user_id': user_id
            },
            UpdateExpression = "set active = :a ",
            ExpressionAttributeValues = {
                ':a': active
            },
            ReturnValues = "UPDATED_NEW"
        )
        return response

    def info_user(self, user_id):
        """Метод запроса информации по ключу партицирования
        """
        table = self.dynamodb.Table(self.table)
        response = table.query(
            ProjectionExpression = 'user_id, name, active',
            KeyConditionExpression = Key('user_id').eq(user_id)
        )
        return response['Items']

    def all_users(self):
        """Метод сканирования всех элементов таблицы.
        """
        table = self.dynamodb.Table(self.table)
        return table.scan()['Items']

    def for_mailer(self, active: list = [1, 2]):
        """Метод выгрузки ключей таблицы для рассылки
        """
        table = self.dynamodb.Table(self.table)
        scan_kwargs = {
            'ProjectionExpression': "user_id, active"
        }
        response = table.scan(**scan_kwargs)

        return [int(item['user_id']) for item in response['Items'] if int(item['active']) in active]

    def delete_note(self, user_id):
        """Метод удаления записи из базы данных.
        """
        table = self.dynamodb.Table(self.table)
        try:
            response = table.delete_item(
                Key = {'user_id': user_id},
                )
            return response

        except Exception as e:
            print('Error', e)


    def delete_table(self):
        """Метод удаления таблицы из базы данных
        """
        table = self.dynamodb.Table(self.table)
        table.delete()