from aiogram import Router, types, F
from aiogram.types import Message, KeyboardButton
from aiogram.types.web_app_info import WebAppInfo
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.filters import Command, StateFilter
from aiogram.utils.keyboard import ReplyKeyboardBuilder

available_food_names = ["суши", "спагетти", "хачапури"]
available_food_sizes = ["маленькую", "среднюю", "большую"]

class OrderFood(StatesGroup):
    waiting_for_food_name = State()
    waiting_for_food_size = State()

router = Router()

@router.message(Command(commands='register'), StateFilter(default_state))
async def cmd_register(message: Message, state: FSMContext):
    kp_build = ReplyKeyboardBuilder()
    buttons: list[KeyboardButton] = [KeyboardButton(text=item) for item in available_food_names]
    kp_build.row(*buttons)
    await state.set_state(OrderFood.waiting_for_food_name.state)
    await message.answer('Can you select food',
                         reply_markup=kp_build.as_markup(resize_keyboard=True))


@router.message(StateFilter(OrderFood.waiting_for_food_name), F.text.isalpha())
async def select_food(message: Message, state: FSMContext):
    await state.update_data(chosen_food=message.text.lower())
    kp_build = ReplyKeyboardBuilder()
    buttons: list[KeyboardButton] = [KeyboardButton(text=item) for item in available_food_sizes]
    kp_build.row(*buttons)
    await state.set_state(OrderFood.waiting_for_food_size.state)
    await message.answer('Select food`s size',
                         reply_markup=kp_build.as_markup(resize_keyboard=True))

@router.message(StateFilter(OrderFood.waiting_for_food_size))
async def select_size(message: Message, state: FSMContext):
    btn = types.KeyboardButton(text='app', web_app=WebAppInfo(url='https://docs.aiogram.dev/en/v2.25.1/telegram/types/reply_keyboard.html'))
    web_app_buton = types.ReplyKeyboardMarkup(keyboard=[[btn]], resize_keyboard=True)
    await state.update_data(size_food=message.text.lower())
    user_data = await state.get_data()
    print(user_data)
    await message.answer(f'{user_data}', reply_markup=web_app_buton)
    await state.finish()
