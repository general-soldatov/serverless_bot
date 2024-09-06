import logging
from aiogram import Dispatcher, F
from aiogram.types import Message, CallbackQuery

from infrastructure.database.user_api import Schedule
from infrastructure.buttons import UserInline, SheduleCall
from infrastructure.lexicon.buttons import BUTTONS_RU
from infrastructure.lexicon.lexicon_ru import USER

log = logging.getLogger(__name__)

def router(dp: Dispatcher):

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
        builder = UserInline().contact()
        await message.answer(USER['contact'], reply_markup=builder)

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