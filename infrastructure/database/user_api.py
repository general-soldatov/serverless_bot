import json
import requests

class UserApi():
    def __init__(self, path='/'):
        pass

    def schedule(self, week: int, day: str, path='schedule.json'):
        with open(path, 'r', encoding='utf-8') as file_json:
            data = json.load(file_json)
            return data[str(week)][day.upper()]

    def contingent(self, name: str):
        url = 'https://storage.yandexcloud.net/termex-bot/json/contingent.json'
        response = requests.get(url)
        data: dict = response.json()
        search_name = name.title()
        if search_name in data.keys():
            return data[search_name]
        return False