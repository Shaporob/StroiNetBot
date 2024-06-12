from aiogram import *
from aiogram.filters import *

from common import admin_list, decoder
from database import db_sqlite3
from common.config_reader import config

router = Router()
bot = Bot(token=config.bot_token.get_secret_value())


@router.message(F.from_user.id.in_(admin_list.list), Command("admin"))
async def admin(message: types.Message):
    reply_message = await message.answer("Вот все обращения на данный момент:")
    user_list = (db_sqlite3.cur.execute("SELECT * FROM users")).fetchall()
    for user in user_list:
        city = decoder.d_city(user[1])
        square = decoder.d_square(user[2])
        budget = decoder.d_budget(user[3])
        user_tg = (await bot.get_chat_member(user[0], user[0])).user
        if user_tg.username:
            user_link = html.link(user_tg.full_name, f"t.me/{user_tg.username}")
        else:
            user_link = html.link(user_tg.full_name, user_tg.url)
        await reply_message.reply(f"\n\n{user_link}\nID: {user[0]}"
                                  f"\nМестоположение: {city}."
                                  f"\nПлощадь: {square}."
                                  f"\nБюджет: {budget}."
                                  f"\nВремя обращения: {user[4]}.", parse_mode="HTML")
