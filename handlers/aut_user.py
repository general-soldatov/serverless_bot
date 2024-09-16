import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from infrastructure.database import UserVar
from infrastructure.database.user_api import Schedule
from infrastructure.configure.config import bot_config
from infrastructure.keyboard import UserInline, SheduleCall
from infrastructure.configure.lexicon import BUTTONS_RU, USER

log = logging.getLogger(__name__)

class Question(StatesGroup):
    question = State()

def router(dp: Dispatcher, bot: Bot):

    @dp.message(F.text == BUTTONS_RU['metodic'])
    async def metodic(message: Message):
        builder = UserInline().metodic()
        await message.answer(USER['metodic'], reply_markup=builder)

    @dp.message(F.text == BUTTONS_RU['textbook'])
    async def metodic(message: Message):
        builder = UserInline().textbook()
        await message.answer(USER['textbook'], reply_markup=builder)

    @dp.message(F.text == BUTTONS_RU['contact'])
    async def contact(message: Message):
        builder = UserInline(width=2).contact()
        await message.answer(USER['contact'], reply_markup=builder)

    @dp.message(Command(commands='profile'))
    async def profile(message: Message):
        user_data = UserVar().get_user(user_id=message.from_user.id)
        await message.answer(USER['profile'].format(name=user_data['name'],
                           profile=user_data['profile'],
                           group=user_data['group'],
                           var=user_data['var']['var_all'],
                           var_d1=user_data['var']['var_d1']))

    @dp.message(F.text == BUTTONS_RU['shedule'])
    async def shedule(message: Message):
        builder = UserInline(width=2).shedule()
        weekday, shedules = Schedule()(day='today')
        text = weekday + '\n'
        text += '\n'.join([f'{key}: {value}' for key, value in shedules.items()])
        await message.answer(text, reply_markup=builder)

    @dp.callback_query(SheduleCall.filter())
    async def shedule_call(callback: CallbackQuery,
                           callback_data: SheduleCall):
        builder = UserInline(width=2).shedule(day=callback_data.day)
        weekday, shedules = Schedule()(day=callback_data.day)
        text = weekday + '\n'
        text += '\n'.join([f'{key}: {value}' for key, value in shedules.items()])
        await callback.message.edit_text(text=text, reply_markup=builder)


    @dp.callback_query(F.data == 'question')
    async def question(callback: CallbackQuery, state: FSMContext):
        await callback.message.edit_text(text=USER['question'])
        await state.set_state(Question.question.state)

    @dp.message(StateFilter(Question.question))
    async def get_question(message: Message, state: FSMContext):
        try:
            data = UserVar().get_user(int(message.from_user.id))
            button = UserInline().question(user_id=int(message.from_user.id))
            await message.answer(text=USER['get_question'])
            await bot.send_message(chat_id=bot_config.admin_ids,
                                text=USER['send_question'].format(name=data['name'],
                                                                    profile=data['profile'],
                                                                    group=data['group'],
                                                                    user_id=message.from_user.id),
                                reply_markup=button)
            await bot.copy_message(chat_id=bot_config.admin_ids,
                                from_chat_id=message.from_user.id,
                                message_id=message.message_id)
        except KeyError:
            await message.answer(text=USER['permission_denied'])
        await state.clear()