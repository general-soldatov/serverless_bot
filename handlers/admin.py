import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter

from infrastructure.configure.config import bot_config
from infrastructure.database import UserVar, UserUn
from infrastructure.lexicon.buttons import BUTTONS_RU
from infrastructure.lexicon.lexicon_ru import ADMIN
from infrastructure.keyboard import AdminInline, MailGroup, Available

logger = logging.getLogger(__name__)

class Mailer(StatesGroup):
    profile = State()
    group = State()
    confirmation = State()


def router(dp: Dispatcher, bot: Bot):
    @dp.message(F.text == BUTTONS_RU['mailer'], StateFilter(default_state), F.from_user.id == int(bot_config.admin_ids))
    async def mailer(message: types.Message, state: FSMContext):
        buttons = AdminInline(width=4).mailer_profile()
        await message.answer(text=ADMIN['mailer'], reply_markup=buttons)
        await state.set_state(Mailer.profile.state)


    @dp.callback_query(MailGroup.filter(), StateFilter(Mailer.profile), F.from_user.id == int(bot_config.admin_ids))
    async def callback_mailer(callback: types.CallbackQuery,
                              callback_data: MailGroup, state: FSMContext):
        if callback_data.profile == BUTTONS_RU['all']:
            await callback.message.edit_text(text=ADMIN['message_mailer'])
            await state.set_data(data={'profile': 'all', 'group': '0'})
            await state.set_state(Mailer.group.state)
        elif callback_data.group == '0':
            buttons = AdminInline(width=4).mailer_group(profile=callback_data.profile)

    @dp.message(StateFilter(Mailer.group), F.from_user.id == int(bot_config.admin_ids))
    async def message_mailer(message: types.Message, state: FSMContext):
        button = AdminInline().available(message_id=message.message_id)
        await message.answer(text=ADMIN['available'], reply_markup=button)
        await state.set_state(Mailer.confirmation.state)

    @dp.callback_query(Available.filter(), StateFilter(Mailer.confirmation), F.from_user.id == int(bot_config.admin_ids))
    async def mailer_confirmation(callback: types.CallbackQuery,
                                  callback_data: Available, state: FSMContext):
        data = await state.get_data()
        if callback_data.go:
            if data['profile'] == 'all':
                for item in UserUn().for_mailer():
                    try:
                        print(item)
                        await bot.copy_message(from_chat_id=callback.from_user.id,
                                               chat_id=item,
                                               message_id=callback_data.message_id)
                    except Exception as e:
                        logger.error(e)
        await state.clear()
        await callback.answer()
