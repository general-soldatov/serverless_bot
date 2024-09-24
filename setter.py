import json
import time
from progress.bar import IncrementalBar
from infrastructure.database import UserSheet, UserVar, UserUn, YDBStorage
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


def writer_toml(text):
    with open('infrastructure/configure/lexicon.toml', 'a', encoding='utf-8') as file:
        text = toml.dumps(text)
        file.write(text)
        print('Succesful')

def dump_write():
    """Функция переноса user_id из дампа в базу данных
    """
    data = []
    with open('base.txt', 'r', encoding='utf-8') as file:
        for item in file:
            user = item.strip().split()[1]

            if user not in data:
                data.append(user)
        data.pop(0)
        bar = IncrementalBar('DB Record', max=len(data))
        for i, item in enumerate(data):
            UserUn().put_item(user_id=int(item), name=f'New user_{i}')
            bar.next()
            time.sleep(0.5)

        print(' Success')


def create_tables():
    """Функция для создания таблиц в БД
    """
    UserUn().create_table()
    time.sleep(1)
    YDBStorage()._create_table()
    time.sleep(1)
    UserVar().create_table()


# create_tables()
# dump_write()

print(UserVar().all_users())