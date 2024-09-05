from aiogram import Dispatcher, types, F
from aiogram.types import Message, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.filters import Command, StateFilter
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from infrastructure.buttons import UserButton
from infrastructure.database import UserApi, UserUn
from infrastructure.lexicon.lexicon_ru import COMANDS, USER
from infrastructure.lexicon.buttons import BUTTONS_RU

available = ['no', 'yes']

class Register(StatesGroup):
    name_user = State()
    confirmation = State()

def router(dp: Dispatcher):

    @dp.message(Command(commands='register'))
    async def cmd_register(message: Message, state: FSMContext):
        await state.set_state(Register.name_user.state)
        await message.answer(COMANDS['register'])


    @dp.message(StateFilter(Register.name_user))
    async def user_name(message: Message, state: FSMContext):
        user = UserApi().contingent(name=message.text)
        if user:
            kp_build = ReplyKeyboardBuilder()
            buttons: list[KeyboardButton] = [KeyboardButton(text=BUTTONS_RU[item]) for item in available]
            kp_build.row(*buttons)
            user['name'] = message.text.title()
            await state.set_data(data=user)
            await state.set_state(Register.confirmation.state)
            await message.answer(USER['available'].format(name=user['name'],
                                                        profile=user['profile'],
                                                        group=user['group']),
                                reply_markup=kp_build.as_markup(resize_keyboard=True))
        else:
            await message.answer(USER['uncorrect'])

    @dp.message(StateFilter(Register.confirmation), F.text == BUTTONS_RU['yes'])
    async def app_user(message: Message, state: FSMContext):
        register = UserUn()
        register.update_active(user_id=message.from_user.id, active=2)
        button_markup = UserButton().auth_user()
        user_data = await state.get_data()
        await message.answer(f'{user_data}', reply_markup=button_markup)
        await state.clear()

    @dp.message(StateFilter(Register.confirmation), F.text == BUTTONS_RU['no'])
    async def no_user(message: Message, state: FSMContext):
        await message.answer(text=USER['no'])
        await state.set_state(Register.name_user.state)
