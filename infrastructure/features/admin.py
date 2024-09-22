import logging

from aiogram import Bot, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.exceptions import TelegramAPIError

from infrastructure.database import UserUn, UserVar
from infrastructure.configure.lexicon import ADMIN, BUTTONS_RU, USER
from infrastructure.keyboard.inline_but import Available, AdminInline, PrizeGroup

logger = logging.getLogger(__name__)

class Mailer(StatesGroup):
    profile = State()
    group = State()
    confirmation = State()

class QuestionReply(StatesGroup):
    reply = State()
    available = State()

class PrizeStudents(StatesGroup):
    profile = State()
    group = State()
    score = State()

class AdminFeatures:
    def __init__(self, bot: Bot):
        self.bot = bot

    async def select_mail(self, callback: types.CallbackQuery,
                                  callback_data: Available, state: FSMContext):
        if callback_data.profile == BUTTONS_RU['all']:
            await callback.message.edit_text(text=ADMIN['message_mailer'])
            await state.set_data(data={'profile': 'all', 'group': '0'})
            await state.set_state(Mailer.group.state)
        elif callback_data.group == '0':
            buttons = AdminInline(width=4).mailer_group(profile=callback_data.profile)
            await callback.message.edit_text(text=ADMIN['mail_group'], reply_markup=buttons)
            await state.set_state(Mailer.profile.state)
        else:
            await callback.message.edit_text(text=ADMIN['message_mailer'])
            await state.set_data(data={'profile': callback_data.profile, 'group': callback_data.group})
            await state.set_state(Mailer.group.state)

    async def mailer(self, callback: types.CallbackQuery,
                                  callback_data: Available, state: FSMContext):
        data = await state.get_data()
        errors = {}
        if data['profile'] == 'all':
            for item in UserUn().for_mailer():
                try:
                    await self.bot.copy_message(from_chat_id=callback.from_user.id,
                                            chat_id=item,
                                            message_id=callback_data.message_id)
                except TelegramAPIError as e:
                    if 'Bad Request: chat not found' in e.__str__():
                        UserUn().update_active(user_id=item, active=0)
                        errors[item] = e
                        logger.error(e)

                except Exception as e:
                    logger.error(e)
                    errors[item] = e

        else:
            user = UserVar().for_mailer(profile=data['profile'], group=data['group'])
            if user:
                for item in user:
                    try:
                        await self.bot.copy_message(from_chat_id=callback.from_user.id,
                                            chat_id=item,
                                            message_id=callback_data.message_id)

                    except Exception as e:
                        logger.error(e)
                        errors[item] = e

            else:
                errors['all'] = 'not users'
        await callback.message.edit_text(text=ADMIN['mailer_done'].format(errors=errors))


    async def reply_question(self, callback: types.CallbackQuery,
                                  callback_data: Available, state: FSMContext):
        data = await state.get_data()
        try:
            await self.bot.send_message(chat_id=data['user_id'], text=ADMIN['send_question'])
            await self.bot.copy_message(chat_id=data['user_id'],
                                    from_chat_id=callback.from_user.id,
                                    message_id=callback_data.message_id)
            await callback.message.edit_text(text=ADMIN['question_succesful'].format(user_id=data['user_id']))
        except Exception as e:
            logger.error(e)
            await callback.message.edit_text(text=ADMIN['question_error'].format(error=e))

    async def select_score(self, callback: types.CallbackQuery,
                                  callback_data: PrizeGroup, state: FSMContext):
        if callback_data.profile == BUTTONS_RU['all']:
            buttons = AdminInline(width=2).lst_study()
            await callback.message.edit_text(text=ADMIN['stat_info'], reply_markup=buttons)

        elif callback_data.group == '0':
            buttons = AdminInline(width=4).mailer_group(profile=callback_data.profile, Group=PrizeGroup)
            await callback.message.edit_text(text=ADMIN['score_group'], reply_markup=buttons)
            # await state.set_state(PrizeStudents.profile.state)
        else:
            buttons = AdminInline(width=2).lst_study(callback_data.profile, callback_data.group)
            await callback.message.edit_text(text=ADMIN['stat_info'], reply_markup=buttons)
            # await state.set_data(data={'profile': callback_data.profile, 'group': callback_data.group})
            # await state.set_state(PrizeStudents.group.state)

    async def set_score(self, message: types.Message, state: FSMContext):
        data = await state.get_data()
        if message.text[0] == '+':
            UserVar().set_prize(user_id=data['user_id'], prize=int(message.text[1:]))
        elif message.text[0] == '-':
            UserVar().set_fine(user_id=data['user_id'], fine=int(message.text[1:]))
        else:
            await message.delete()
            await message.answer(USER['uncorrect'])
            return
        await message.answer(ADMIN['success_score'])
        await state.clear()
