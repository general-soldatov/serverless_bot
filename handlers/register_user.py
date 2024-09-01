from aiogram import Dispatcher, types
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup, default_state
from aiogram.dispatcher.filters import Command, CommandStart, StateFilter, Text

available_food_names = ["суши", "спагетти", "хачапури"]
available_food_sizes = ["маленькую", "среднюю", "большую"]

class OrderFood(StatesGroup):
    waiting_for_food_name = State()
    waiting_for_food_size = State()

async def register_user(dp: Dispatcher):
    @dp.message_handler(Command(commands='register'), state='*')
    async def cmd_register(message: Message, state: FSMContext):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for name in available_food_names:
            keyboard.add(name)
        await state.set_state(OrderFood.waiting_for_food_name.state)
        await message.answer('Can you select food', reply_markup=keyboard)


    @dp.message_handler(state=OrderFood.waiting_for_food_name)
    async def select_food(message: Message, state: FSMContext):
        await state.update_data(chosen_food=message.text.lower())
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for size in available_food_sizes:
            keyboard.add(size)
        await state.set_state(OrderFood.waiting_for_food_size.state)
        await message.answer('Select food`s size', reply_markup=keyboard)

    @dp.message_handler(state=OrderFood.waiting_for_food_size)
    async def select_size(message: Message, state: FSMContext):
        await state.update_data(size_food=message.text.lower())
        user_data = await state.get_data()
        print(user_data)
        await message.answer(f'{user_data}')
        await state.finish()
