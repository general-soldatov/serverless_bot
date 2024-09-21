from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from infrastructure.configure.lexicon import BUTTONS_RU
from infrastructure.database import UserVar
from infrastructure.configure.config import ButtonConfig, StudyConfig, AdminConfig

class InlineKeyboard:
    def __init__(self, width: int = 3, resize_keyboard: bool = True):
        self.width = width
        self.resize_keyboard = resize_keyboard
        self.button = ButtonConfig()
        self.study = StudyConfig()

    @staticmethod
    def builder_row(buttons: list[InlineKeyboardButton], width: int = 3) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.row(*buttons, width=width)
        return builder.as_markup()


class SheduleCall(CallbackData, prefix='shedule'):
    day: str

class GraphTaskCall(CallbackData, prefix='graph_task'):
    task: str
    name: str

class GraphTaskScoreCall(CallbackData, prefix='p_t'):
    task: str
    score: str
    user_id: str
    name: str

class UserQuestion(CallbackData, prefix='faq'):
    user_id: int

class UserInline(InlineKeyboard):

    def metodic(self) -> InlineKeyboardMarkup:
        books: dict = self.button.metodic
        buttons: list = [InlineKeyboardButton(text=BUTTONS_RU[key], url=value) for key, value in books.items()]
        return self.builder_row(buttons=buttons, width=self.width)

    def textbook(self) -> InlineKeyboardMarkup:
        books: dict = self.button.books
        buttons: list = [InlineKeyboardButton(text=BUTTONS_RU[key], url=value) for key, value in books.items()]
        return self.builder_row(buttons=buttons, width=self.width)

    def contact(self) -> InlineKeyboardMarkup:
        contacts: dict = self.button.contact
        buttons: list = [InlineKeyboardButton(text=BUTTONS_RU[key], url=value) for key, value in contacts.items()]
        buttons.append(InlineKeyboardButton(text=BUTTONS_RU['question'], callback_data='question'))
        return self.builder_row(buttons=buttons, width=self.width)

    def question(self, user_id: int) -> InlineKeyboardMarkup:
        buttons: list = [InlineKeyboardButton(text=BUTTONS_RU['send'], callback_data=UserQuestion(user_id=user_id).pack())]
        return self.builder_row(buttons=buttons, width=self.width)

    def shedule(self, day:str = 'today') -> InlineKeyboardMarkup:
        days: dict = self.study.select_day
        days.remove(day)
        buttons: list = [InlineKeyboardButton(text=BUTTONS_RU[item],
                                              callback_data=SheduleCall(day=item).pack()) for item in days]
        return self.builder_row(buttons=buttons, width=self.width)

    def graph_task(self, user_id) -> InlineKeyboardMarkup:
        task = list(self.study.tasks)
        data: dict = UserVar().get_user(user_id=int(user_id))
        user: str = data['name'].split(sep=' ')
        name = ' '.join([user[0], user[1][0], user[2][0]])
        for item in data['tasks'].keys():
            task.remove(item)
        buttons: list = [InlineKeyboardButton(text=item,
                                              callback_data=GraphTaskCall(task=item,
                                                                          name=name).pack()) for item in task]
        return self.builder_row(buttons=buttons, width=self.width)

    def prepod_task(self, task, user_id, name, score=9) -> InlineKeyboardMarkup:
        buttons: list = [InlineKeyboardButton(text=str(item),
                                              callback_data=GraphTaskScoreCall(task=task,
                                                                               score=str(item),
                                                                               user_id=user_id, name=name).pack()) for item in range(score)]
        return self.builder_row(buttons=buttons, width=self.width)


class MailGroup(CallbackData, prefix='cr_mail_group'):
    profile: str
    group: str

class Available(CallbackData, prefix='cr_av-le'):
    data: str
    go: bool
    message_id: int

class AdminInline(InlineKeyboard):
    def mailer_profile(self):
        buttons: list = [InlineKeyboardButton(text=str(item),
                                              callback_data=MailGroup(profile=item,
                                                                      group='0').pack()) for item in AdminConfig().profile]
        return self.builder_row(buttons=buttons, width=self.width)

    def mailer_group(self, profile: str):
        group = AdminConfig().group[profile]
        buttons: list = [InlineKeyboardButton(text=str(item),
                                              callback_data=MailGroup(profile=profile,
                                                                      group=item).pack()) for item in group]
        return self.builder_row(buttons=buttons, width=self.width)

    def available(self, message_id, data='mailer'):
        text = ['no', 'yes']
        buttons: list = [InlineKeyboardButton(text=BUTTONS_RU[item],
                                              callback_data=Available(go=i,
                                                                      message_id=message_id,
                                                                      data=data).pack()) for i, item in enumerate(text)]
        return self.builder_row(buttons=buttons, width=self.width)
