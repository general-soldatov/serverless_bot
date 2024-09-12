from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.filters import Command, StateFilter
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from infrastructure.keyboard import UserButton
from infrastructure.database import UserApi, UserUn, UserVar
from infrastructure.lexicon.lexicon_ru import COMANDS, USER
from infrastructure.lexicon.buttons import BUTTONS_RU
from infrastructure.configure.config import bot_config


class Register(StatesGroup):
    name_user = State()
    confirmation = State()

def router(dp: Dispatcher, bot: Bot):

    @dp.message(Command(commands='register'))
    async def cmd_register(message: Message, state: FSMContext):
        await state.set_state(Register.name_user.state)
        await message.answer(COMANDS['register'])


    @dp.message(StateFilter(Register.name_user))
    async def user_name(message: Message, state: FSMContext):
        user = UserApi().contingent(name=message.text)
        if user:
            kp_build = UserButton().user_name()
            user['name'] = message.text.title()
            await state.set_data(data=user)
            await state.set_state(Register.confirmation.state)
            await message.answer(USER['available'].format(name=user['name'],
                                                        profile=user['profile'],
                                                        group=user['group']),
                                reply_markup=kp_build)
        else:
            await message.answer(USER['uncorrect'])

    @dp.message(StateFilter(Register.confirmation), F.text == BUTTONS_RU['yes'])
    async def app_user(message: Message, state: FSMContext):
        register = UserUn()
        register.update_active(user_id=message.from_user.id, active=2)
        button_markup = UserButton().auth_user()
        user_data = await state.get_data()
        UserVar().put_item(user_id=message.from_user.id,
                           name=user_data['name'],
                           profile=user_data['profile'],
                           group=user_data['group'],
                           var=user_data['var'],
                           var_d1=user_data['varD'])
        await message.answer(USER['yes'].format(name=user_data['name'],
                           profile=user_data['profile'],
                           group=user_data['group'],
                           var=user_data['var'],
                           var_d1=user_data['varD']), reply_markup=button_markup)
        await bot.send_message(chat_id=bot_config.admin_ids,
                               text=USER['register_admin'].format(name=user_data['name'],
                                                    profile=user_data['profile'],
                                                    group=user_data['group'],
                                                    var=user_data['var']))
        await state.clear()

    @dp.message(StateFilter(Register.confirmation), F.text == BUTTONS_RU['no'])
    async def no_user(message: Message, state: FSMContext):
        await message.answer(text=USER['no'])
        await state.set_state(Register.name_user.state)
