import json
from infrastructure.database import UserSheet
from infrastructure.database.user_api import UserApi
import requests

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
