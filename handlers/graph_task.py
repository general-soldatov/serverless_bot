from aiogram import Bot, Dispatcher, types, F

from infrastructure.configure.config import bot_config

from infrastructure.lexicon.buttons import BUTTONS_RU
from infrastructure.lexicon.lexicon_ru import USER
from infrastructure.buttons import UserInline, GraphTaskCall, GraphTaskScoreCall

def router(dp: Dispatcher, bot: Bot):
    @dp.message(F.text == BUTTONS_RU['graph_task'])
    async def task(message: types.Message):
        buttons = UserInline(width=6).graph_task()
        await message.answer(text=USER['graph_task'], reply_markup=buttons)

    @dp.callback_query(GraphTaskCall.filter())
    async def graph_task_call(callback: types.CallbackQuery,
                           callback_data: GraphTaskCall):
        button = UserInline(width=7).prepod_task(task=callback_data.task, user_id=str(callback.from_user.id))
        await bot.send_message(chat_id=bot_config.admin_ids,
                               text=USER['graph_task_prepod'].format(task=callback_data.task,
                                                                     name=str(callback.from_user.id)),
                               reply_markup=button)
        await callback.message.edit_text(text=USER['graph_task_call'].format(task=callback_data.task))

    @dp.callback_query(GraphTaskScoreCall.filter())
    async def graph_task_score_call(callback: types.CallbackQuery,
                                    callback_data: GraphTaskScoreCall):
        await bot.send_message(chat_id=callback_data.user_id,
                               text=USER['graph_task_score_user'].format(task=callback_data.task,
                                                                         score=callback_data.score))
        await callback.message.edit_text(
            text=USER['graph_task_score_prepod'].format(name=callback_data.user_id,
                                                        score=callback_data.score,
                                                        task=callback_data.task))
