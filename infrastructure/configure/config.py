import boto3
from dataclasses import dataclass
from dotenv import load_dotenv
from os import getenv

@dataclass
class TgBot:
    token: str
    admin_ids: list[int]
    task_api_url: str
    task_api_token: str
    shedule: str
    contingent: str

class DatabaseConfig:
    endpoint: str
    region_name: str
    key_id: str
    access_key: str
    google_api: str


load_dotenv()
bot_config = TgBot(token=getenv('TOKEN'),
                   admin_ids=getenv('ADMIN_IDS'),
                   task_api_url=getenv('API_TASK'),
                   task_api_token=getenv('API_TASK_TOKEN'),
                   shedule=getenv('API_SHEDULE'),
                   contingent=getenv('API_CONTINGENT'))

database_config = DatabaseConfig(endpoint=getenv('ENDPOINT'),
                                 region_name=getenv('REGION_NAME'),
                                 key_id=getenv('AWS_ACCESS_KEY_ID'),
                                 access_key=getenv('AWS_SECRET_ACCESS_KEY'),
                                 google_api=getenv('GOOGLE_SERVICE_ACCOUNT'))

dynamodb_config = boto3.resource(
                'dynamodb',
                endpoint_url=database_config.endpoint,
                region_name=database_config.region_name,
                aws_access_key_id=database_config.key_id,
                aws_secret_access_key=database_config.access_key
                )