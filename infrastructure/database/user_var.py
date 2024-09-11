import boto3
from boto3.dynamodb.conditions import Key
from os import getenv
from dotenv import load_dotenv

from infrastructure.configure.config import dynamodb_config

class UserVar:
    def __init__(self, dynamodb=None):
        self.dynamodb = dynamodb
        self.table = 'User_Var'
        if not self.dynamodb:
            load_dotenv()
            self.dynamodb = dynamodb_config

    def create_table(self):
        table = self.dynamodb.create_table(
            TableName = self.table,
            KeySchema = [
                {
                    'AttributeName': 'user_id',
                    'KeyType': 'HASH'  # Ключ партицирования
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
                "AttributeName": "profile",
                "AttributeType": "S"
                },
                {
                "AttributeName": "group",
                "AttributeType": "S"
                },

            ]
        )
        return table

    def put_item(self, user_id, name, profile, group, var, var_d1):
        table = self.dynamodb.Table(self.table)
        all_var = {'var_all': var, 'var_d1': var_d1}
        tasks = {'S0': 0}
        bonus = {
            'static': 0,
            'kinematic': 0,
            'dynamic': 0
        }
        response = table.put_item(
            Item = {
                    'user_id': user_id,
                    'name': name,
                    'profile': profile,
                    'group': group,
                    'var': all_var,
                    'tasks': tasks,
                    'bonus': bonus
            }
        )
        return response

    def add_task(self, user_id, task, ball):
        table = self.dynamodb.Table(self.table)
        response = table.update_item(
            Key = {
                'user_id': user_id
            },
            UpdateExpression = f"set tasks.{task} = :t ",
            ExpressionAttributeValues = {
                ':t': ball
            },
            ReturnValues = "UPDATED_NEW"
        )
        return response

    def get_user(self, user_id):
        """Метод запроса информации о пользователе по ключу партицирования
        """
        table = self.dynamodb.Table(self.table)
        response = table.get_item(
            Key = {
                'user_id': user_id
            }
        )
        return response['Item']

    def add_bonus(self, user_id, category, task):
        table = self.dynamodb.Table(self.table)
        response = table.update_item(
            Key = {
                'user_id': user_id
            },
            UpdateExpression = f"set bonus.{category} = :b ",
            ExpressionAttributeValues = {
                ':b': task
            },
            ReturnValues = "UPDATED_NEW"
        )
        return response


    def all_users(self):
        table = self.dynamodb.Table(self.table)
        return table.scan()['Items']

    def delete_note(self, user_id):
        table = self.dynamodb.Table(self.table)
        try:
            response = table.delete_item(
                Key = {'user_id': user_id},
                )
            return response

        except Exception as e:
            print('Error', e)


    def delete_table(self):
        table = self.dynamodb.Table(self.table)
        table.delete()