import json
from infrastructure.database import UserSheet, UserVar
from infrastructure.database.user_api import UserApi
import requests
import toml
from infrastructure.configure.config import ButtonConfig, StudyConfig
from infrastructure.database.user_api import Schedule
from infrastructure.configure.lexicon import USER, ADMIN, COMMANDS

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

# lst_task: list = list(task_head.keys())
# data: dict = UserVar().get_user(user_id=980314213)
# for item in data['tasks'].keys():
#     lst_task.remove(item)
# print(data['name'], lst_task)
# print(UserVar().delete_note(122))
def writer_toml(text):
    with open('infrastructure/configure/lexicon.toml', 'a', encoding='utf-8') as file:
        text = toml.dumps(text)
        file.write(text)
        print('Succesful')

# weekday, shedules = Schedule()(day='today')
# print(weekday, shedules)

# UserVar().set_fine(user_id=943385782, fine=0)
# 154666  23455
UserVar().put_item(user_id=23455, name='Yurk Dll Siii', profile='НТТС', group='8-а', var=12, var_d1=1)