import requests
from datetime import datetime, timedelta
from os import getenv

from infrastructure.configure.config import bot_config

class UserApi():
    def __init__(self, path='/'):
        pass

    def schedule(self, week: int, day: str):
        response = requests.get(bot_config.shedule)
        data: dict = response.json()
        return data[str(week)][day.upper()]

    def contingent(self, name: str) -> dict | bool:
        response = requests.get(bot_config.contingent)
        data: dict = response.json()
        search_name = name.title()
        return data.get(search_name, False)

    def get_task(self, category='mechanic', level=10, num=0):
        token = bot_config.task_api_token
        api_url = bot_config.task_api_url
        url = f'{api_url}/task_book/token={token}category={category}_level={level}num={num}'
        response = requests.get(url)
        return response.json()

class Schedule:
    def __init__(self, connect=UserApi()) -> None:
        self.connect = connect
        self.weekdays = ['', "ПОНЕДЕЛЬНИК", "ВТОРНИК", "СРЕДА", "ЧЕТВЕРГ", "ПЯТНИЦА", "СУББОТА", "ВОСКРЕСЕНЬЕ"]

    def __call__(self, day: str) -> str:
        days = ['today', 'tomorrow', 'after_tom', 'to_2_day']
        date_to = days.index(day)
        calendar = self.go_day(date_to)
        shedule: dict = self.connect.schedule(week=((calendar.week+1) % 2),
                              day=self.weekdays[calendar.weekday])
        return self.weekdays[calendar.weekday], shedule

    @staticmethod
    def go_day(day):
        need_day = datetime.now() + timedelta(days=day)
        return need_day.isocalendar()
