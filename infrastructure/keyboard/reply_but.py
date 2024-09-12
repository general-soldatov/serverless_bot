from aiogram import types, F
from aiogram.filters.callback_data import CallbackData
from aiogram.types import KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram.types.web_app_info import WebAppInfo
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from infrastructure.lexicon.buttons import BUTTONS_RU
from infrastructure.database import UserUn, UserVar
from infrastructure.configure.config import ButtonConfig, StudyConfig

class UserButton:
    def __init__(self, width=3, resize_keyboard=True):
        self.width = width
        self.resize_keyboard = resize_keyboard

    def __call__(self, user_id):
        self.user = UserUn().info_user(user_id)
        if self.user[0]['active'] == 3:
            return self.auth_user()
        if self.user[0]['active'] == 2:
            return self.auth_user()
        if self.user[0]['active'] == 1:
            return self.unauth_user()
        return False

    def user_name(self) -> ReplyKeyboardMarkup:
        available = ['no', 'yes']
        kp_build = ReplyKeyboardBuilder()
        buttons: list[KeyboardButton] = [KeyboardButton(text=BUTTONS_RU[item]) for item in available]
        kp_build.row(*buttons)
        return kp_build.as_markup(resize_keyboard=self.resize_keyboard)

    def auth_user(self) -> ReplyKeyboardMarkup:
        box_button = ['profile', 'metodic', 'textbook', 'graph_task', 'shedule', 'contact']
        kp_build = ReplyKeyboardBuilder()
        btn = types.KeyboardButton(text=BUTTONS_RU[box_button[0]], web_app=WebAppInfo(url='https://docs.aiogram.dev/en/v2.25.1/telegram/types/reply_keyboard.html'))
        buttons: list[KeyboardButton] = [btn]
        buttons.extend([KeyboardButton(text=BUTTONS_RU[item]) for item in box_button[1:]])
        kp_build.row(*buttons, width=self.width)
        return kp_build.as_markup(resize_keyboard=self.resize_keyboard)

    def admin_user(self) -> ReplyKeyboardMarkup:
        pass

    def unauth_user(self) -> ReplyKeyboardMarkup:
        box_button = ['metodic', 'textbook', 'contact']
        kp_build = ReplyKeyboardBuilder()
        buttons: list[KeyboardButton] = [KeyboardButton(text=BUTTONS_RU[item]) for item in box_button]
        kp_build.row(*buttons, width=self.width)
        return kp_build.as_markup(resize_keyboard=self.resize_keyboard)

# class SheduleCall(CallbackData, prefix='shedule'):
#     day: str

# class GraphTaskCall(CallbackData, prefix='graph_task'):
#     task: str
#     name: str

# class GraphTaskScoreCall(CallbackData, prefix='p_t'):
#     task: str
#     score: str
#     user_id: str
#     name: str


# class UserInline:
#     def __init__(self, width: int = 3, resize_keyboard: bool = True):
#         self.width = width
#         self.resize_keyboard = resize_keyboard
#         self.button = ButtonConfig()
#         self.study = StudyConfig()

#     def metodic(self) -> InlineKeyboardMarkup:
#         builder = InlineKeyboardBuilder()
#         books: dict = self.button.metodic
#         buttons: list = [InlineKeyboardButton(text=BUTTONS_RU[key], url=value) for key, value in books.items()]
#         builder.row(*buttons, width=self.width)
#         return builder.as_markup()

#     def textbook(self) -> InlineKeyboardMarkup:
#         builder = InlineKeyboardBuilder()
#         books: dict = self.button.metodic
#         buttons: list = [InlineKeyboardButton(text=BUTTONS_RU[key], url=value) for key, value in books.items()]
#         builder.row(*buttons, width=self.width)
#         return builder.as_markup()

#     def contact(self) -> InlineKeyboardMarkup:
#         builder = InlineKeyboardBuilder()
#         contacts: dict = self.button.contact
#         buttons: list = [InlineKeyboardButton(text=BUTTONS_RU[key], url=value) for key, value in contacts.items()]
#         builder.row(*buttons, width=self.width)
#         return builder.as_markup()

#     def shedule(self, day:str = 'today') -> InlineKeyboardMarkup:
#         builder = InlineKeyboardBuilder()
#         days: dict = self.study.select_day
#         days.remove(day)
#         buttons: list = [InlineKeyboardButton(text=BUTTONS_RU[item],
#                                               callback_data=SheduleCall(day=item).pack()) for item in days]
#         builder.row(*buttons, width=self.width)
#         return builder.as_markup()

#     def graph_task(self, user_id) -> InlineKeyboardMarkup:
#         builder = InlineKeyboardBuilder()
#         task = list(self.study.tasks)
#         data: dict = UserVar().get_user(user_id=int(user_id))
#         user: str = data['name'].split(sep=' ')
#         name = ' '.join([user[0], user[1][0], user[2][0]])
#         for item in data['tasks'].keys():
#             task.remove(item)
#         buttons: list = [InlineKeyboardButton(text=item,
#                                               callback_data=GraphTaskCall(task=item,
#                                                                           name=name).pack()) for item in task]
#         builder.row(*buttons, width=self.width)
#         return builder.as_markup()

#     def prepod_task(self, task, user_id, name) -> InlineKeyboardMarkup:
#         builder = InlineKeyboardBuilder()
#         buttons: list = [InlineKeyboardButton(text=str(item),
#                                               callback_data=GraphTaskScoreCall(task=task,
#                                                                                score=str(item),
#                                                                                user_id=user_id, name=name).pack()) for item in range(self.width)]
#         builder.row(*buttons, width=self.width)
#         return builder.as_markup()
