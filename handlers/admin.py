from aiogram import Bot, Dispatcher, types, F

from infrastructure.configure.config import bot_config
from infrastructure.database import UserVar
from infrastructure.lexicon.buttons import BUTTONS_RU
from infrastructure.lexicon.lexicon_ru import USER
from infrastructure.keyboard import UserInline, GraphTaskCall, GraphTaskScoreCall

def router(dp: Dispatcher, bot: Bot):
    @dp.message(F.text == BUTTONS_RU['mailer'], F.from_user.id == bot_config.admin_ids)
    async def mailer(message: types.Message):
        await message.answer(text=USER['permission_denied'])
        await bot.send_message(chat_id=bot_config.admin_ids, text='str(e)')
