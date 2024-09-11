import json
from infrastructure.database import UserSheet
from infrastructure.database.user_api import UserApi
import requests
from infrastructure.configure.config import ButtonConfig

def schedule_json():
    data = UserSheet(user_id='333').shedule()

    with open('schedule.json', 'w', encoding='utf-8') as files:
        json.dump(data, files, ensure_ascii=False, indent=4)
        print('Succesful')

def contingent_json():
    data = UserSheet(user_id='33').contingent()

    with open('contingent.json', 'w', encoding='utf-8') as files:
        json.dump(data, files, ensure_ascii=False, indent=4)
        print('Succesful')

task_head = {
            'S1': 'E', 'S2': 'F', 'S3': 'G', 'S4': 'H', 'S5': 'I', 'S6': 'J',
            'K1': 'K', 'K2': 'L', 'K3': 'M', 'K4': 'N', 'K5': 'O',
            'D1': 'P', 'D2': 'Q', 'D3': 'R', 'D4': 'S', 'D5': 'T', 'D6': 'U'
            }

print(ButtonConfig().__dict__)
