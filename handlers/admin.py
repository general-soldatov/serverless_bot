import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram.exceptions import TelegramAPIError

from infrastructure.configure.config import bot_config
from infrastructure.database import UserVar, UserUn
from infrastructure.lexicon.buttons import BUTTONS_RU
from infrastructure.lexicon.lexicon_ru import ADMIN
from infrastructure.keyboard import AdminInline, MailGroup, Available
from infrastructure.features import AdminFeatures, Mailer

logger = logging.getLogger(__name__)


def router(dp: Dispatcher, bot: Bot):
    @dp.message(F.text == BUTTONS_RU['mailer'], StateFilter(default_state), F.from_user.id == int(bot_config.admin_ids))
    async def mailer(message: types.Message, state: FSMContext):
        buttons = AdminInline(width=4).mailer_profile()
        await message.answer(text=ADMIN['mailer'], reply_markup=buttons)
        await state.set_state(Mailer.profile.state)


    @dp.callback_query(MailGroup.filter(), StateFilter(Mailer.profile), F.from_user.id == int(bot_config.admin_ids))
    async def callback_mailer(callback: types.CallbackQuery,
                              callback_data: MailGroup, state: FSMContext):
        await AdminFeatures(bot).select_mail(callback, callback_data, state)


    @dp.message(StateFilter(Mailer.group), F.from_user.id == int(bot_config.admin_ids))
    async def message_mailer(message: types.Message, state: FSMContext):
        button = AdminInline().available(message_id=message.message_id)
        data = await state.get_data()
        await message.answer(text=ADMIN['available'].format(profile=data['profile'],
                                                            group=data['group']), reply_markup=button)
        await state.set_state(Mailer.confirmation.state)

    @dp.callback_query(Available.filter(), StateFilter(Mailer.confirmation), F.from_user.id == int(bot_config.admin_ids))
    async def mailer_confirmation(callback: types.CallbackQuery,
                                  callback_data: Available, state: FSMContext):
        await AdminFeatures(bot).mailer(callback, callback_data, state)
        await state.clear()
        await callback.answer()
