import requests
from datetime import datetime, timedelta

class UserApi():
    def __init__(self, path='/'):
        pass

    def schedule(self, week: int, day: str):
        url = 'https://storage.yandexcloud.net/termex-bot/json/schedule.json'
        response = requests.get(url)
        data: dict = response.json()
        return data[str(week)][day.upper()]

    def contingent(self, name: str) -> dict | bool:
        url = 'https://storage.yandexcloud.net/termex-bot/json/contingent.json'
        response = requests.get(url)
        data: dict = response.json()
        search_name = name.title()
        if search_name in data.keys():
            return data[search_name]
        return False

class Schedule:
    def __init__(self, connect=UserApi()) -> None:
        self.connect = connect
        self.weekdays = ["ПОНЕДЕЛЬНИК", "ВТОРНИК", "СРЕДА", "ЧЕТВЕРГ", "ПЯТНИЦА", "СУББОТА", "ВОСКРЕСЕНЬЕ"]

    def __call__(self, day: str) -> str:
        days = ['today', 'tomorrow', 'after_tom']
        date_to = days.index(day)
        calendar = self.go_day(date_to)
        shedule: dict = self.connect.schedule(week=calendar.week,
                              day=self.weekdays[calendar.weekday])
        return self.weekdays[calendar.weekday], shedule

    @staticmethod
    def go_day(day):
        need_day = datetime.now() + timedelta(days=day)
        return need_day.isocalendar()
