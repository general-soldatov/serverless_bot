from aiogram import types, F
from aiogram.filters.callback_data import CallbackData
from aiogram.types import KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram.types.web_app_info import WebAppInfo
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from infrastructure.lexicon.buttons import BUTTONS_RU
from infrastructure.database import UserUn

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
        box_button = ['profile', 'metodic', 'textbook', 'shedule', 'contact']
        kp_build = ReplyKeyboardBuilder()
        btn = types.KeyboardButton(text=BUTTONS_RU[box_button[0]], web_app=WebAppInfo(url='https://docs.aiogram.dev/en/v2.25.1/telegram/types/reply_keyboard.html'))
        buttons: list[KeyboardButton] = [btn]
        buttons.extend([KeyboardButton(text=BUTTONS_RU[item]) for item in box_button[1:]])
        kp_build.row(*buttons, width=self.width)
        return kp_build.as_markup(resize_keyboard=self.resize_keyboard)

    def unauth_user(self) -> ReplyKeyboardMarkup:
        box_button = ['metodic', 'textbook', 'contact']
        kp_build = ReplyKeyboardBuilder()
        buttons: list[KeyboardButton] = [KeyboardButton(text=BUTTONS_RU[item]) for item in box_button]
        kp_build.row(*buttons, width=self.width)
        return kp_build.as_markup(resize_keyboard=self.resize_keyboard)

class SheduleCall(CallbackData, prefix='shedule'):
    day: str


class UserInline:
    def __init__(self, width: int = 3, resize_keyboard: bool = True):
        self.width = width
        self.resize_keyboard = resize_keyboard

    def metodic(self) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        books = {
            'static': 'https://drive.google.com/file/d/172EuTxLjZlYR0GYi03wdbzu70kae4RdC/view?usp=sharing',
            'kinematic': 'https://drive.google.com/file/d/1i23gh8Kcsu-R5OkyHfdbp7SFUW2c73kx/view?usp=sharing',
            'dynamic': 'https://drive.google.com/file/d/1wrluEFNR18gYT1wFe-oLsmar9pxSB8ZH/view?usp=sharing'
        }
        buttons: list = [InlineKeyboardButton(text=BUTTONS_RU[key], url=value) for key, value in books.items()]
        builder.row(*buttons, width=self.width)
        return builder.as_markup()

    def textbook(self) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        books = {
            'shortcourse': 'https://drive.google.com/file/d/17OhsVDAaPVkdBEMbjl3wR0Scj7WjeMYo/view?usp=drive_link'
        }
        buttons: list = [InlineKeyboardButton(text=BUTTONS_RU[key], url=value) for key, value in books.items()]
        builder.row(*buttons, width=self.width)
        return builder.as_markup()

    def contact(self) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        contacts: dict = {
            'vk': 'https://vk.com/general_soldatov',
            'telegram': 'https://t.me/general_soldatov'
        }
        buttons: list = [InlineKeyboardButton(text=BUTTONS_RU[key], url=value) for key, value in contacts.items()]
        builder.row(*buttons, width=self.width)
        return builder.as_markup()

    def shedule(self, day:str = 'today') -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        days: dict = ['today', 'tomorrow', 'after_tom']
        days.remove(day)
        buttons: list = [InlineKeyboardButton(text=BUTTONS_RU[item],
                                              callback_data=SheduleCall(day=item).pack()) for item in days]
        builder.row(*buttons, width=self.width)
        return builder.as_markup()