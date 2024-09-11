from aiogram import Bot, Dispatcher, types, F

from infrastructure.configure.config import bot_config
from infrastructure.database import UserVar
from infrastructure.lexicon.buttons import BUTTONS_RU
from infrastructure.lexicon.lexicon_ru import USER
from infrastructure.buttons import UserInline, GraphTaskCall, GraphTaskScoreCall

def router(dp: Dispatcher, bot: Bot):
    @dp.message(F.text == BUTTONS_RU['graph_task'])
    async def task(message: types.Message):
        try:
            buttons = UserInline(width=6).graph_task(user_id=message.from_user.id)
            await message.answer(text=USER['graph_task'], reply_markup=buttons)
        except KeyError:
            await message.answer(text=USER['permission_denied'], reply_markup=buttons)
        except Exception as e:
            await bot.send_message(chat_id=bot_config.admin_ids, text=str(e))

    @dp.callback_query(GraphTaskCall.filter())
    async def graph_task_call(callback: types.CallbackQuery,
                           callback_data: GraphTaskCall):
        button = UserInline(width=7).prepod_task(task=callback_data.task,
                                                 user_id=str(callback.from_user.id),
                                                 name=callback_data.name)
        await bot.send_message(chat_id=bot_config.admin_ids,
                               text=USER['graph_task_prepod'].format(task=callback_data.task,
                                                                     name=callback_data.name), reply_markup=button)
        await callback.message.edit_text(text=USER['graph_task_call'].format(task=callback_data.task))

    @dp.callback_query(GraphTaskScoreCall.filter())
    async def graph_task_score_call(callback: types.CallbackQuery,
                                    callback_data: GraphTaskScoreCall):
        UserVar().add_task(user_id=int(callback_data.user_id),
                           task=callback_data.task,
                           ball=callback_data.score)
        await bot.send_message(chat_id=callback_data.user_id,
                               text=USER['graph_task_score_user'].format(task=callback_data.task,
                                                                         score=callback_data.score))
        await callback.message.edit_text(
            text=USER['graph_task_score_prepod'].format(name=callback_data.name,
                                                        score=callback_data.score,
                                                        task=callback_data.task))
