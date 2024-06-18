import asyncio
import datetime

from aiogram import *
from aiogram.filters import *

import kbds.reply as reply
from kbds import inline
from common import decoder, admin_list
from database import db_sqlite3
from common.config_reader import config

router = Router()

bot = Bot(token=config.bot_token.get_secret_value())


@router.message(F.text, Command("start"))
async def start(message: types.Message):
    await message.answer("Добрый день! Вас приветствует компания <b>«СтройНет»</b>. Для выяснения подробной "
                         "информации выберите в меню ниже желаемое действие.", reply_markup=reply.get_menu(),
                         parse_mode="HTML")


@router.message(F.text == "О нас")
async def about(message: types.Message):
    await message.reply(
        f"Мы – компания <b>«СтройНет»</b>, специализирующаяся на стройке различных частных домов и пристройкам к ним. "
        f"Мы работаем на рынке более 20 лет, имея на счету множество успешных проектов с отличными отзывами.",
        parse_mode="HTML")


@router.message(F.text == "Примеры наших работ")
async def examples(message: types.Message):
    example_1 = types.FSInputFile("media/example_1.png")
    example_2 = types.FSInputFile("media/example_2.png")
    example_3 = types.FSInputFile("media/example_3.png")
    reply_message = await message.reply("Вот несколько примеров наших последних работ:")
    await asyncio.sleep(0.5)
    await reply_message.reply_photo(example_1, "Москва, 2022 год.")
    await asyncio.sleep(4)
    await reply_message.reply_photo(example_2, "Санкт-Петербург, 2020 год.")
    await asyncio.sleep(4)
    await reply_message.reply_photo(example_3, "Екатеринбург, 2023 год.")
    await asyncio.sleep(4)


@router.message(F.text == "Связь с менеджером")
async def manager_link(message: types.Message):
    await message.reply("Вот контакт нашего менеджера:", reply_markup=inline.get_manager_link())


@router.message(F.text == "Основатель фирмы")
async def manager_link(message: types.Message):
    founder = types.FSInputFile("media/founder.png")
    await message.reply_photo(founder, f"Основателем нашей фирмы является <b>Игорь Игнатков</b> – "
                                       f"российский бизнесмен, основавший компанию <b>«СтройНет»</b> в 1998 году."
                                       f"Он находится на 44 месте по состоянию среди "
                                       f"российских бизнесменов в списке Forbes.",
                              reply_markup=inline.get_founder_link(), parse_mode="HTML")


@router.message(F.text == "Купить дом")
async def question(message: types.Message):
    reply_message = await message.reply("Давайте для начала пройдём небольшой опрос.", reply_markup=reply.delete_menu())
    await asyncio.sleep(0.5)
    await reply_message.delete()
    await message.reply("Давайте для начала пройдём небольшой опрос.\n<b>Вы согласны?</b>",
                        parse_mode="HTML", reply_markup=inline.question_yes_no())


@router.callback_query(F.data == "question_cancel")
async def question_cansel(callback: types.CallbackQuery):
    await callback.message.answer("<i>Отмена.</i>\n\n<b>Обращайтесь позже!</b>", parse_mode="HTML")
    await start(callback.message)


@router.callback_query(F.data == "question_yesno_yes")
async def question_yesno_yes(callback: types.CallbackQuery):
    await callback.message.answer("<i>Вы согласны пройти опрос? – Да!</i>\n\n"
                                     "<b>Где вы планируете построить дом?</b>",
                                     parse_mode="HTML", reply_markup=inline.question_home_location())


@router.callback_query(inline.QuestionHomeSquareData.filter())
async def question_home_square(callback: types.CallbackQuery, callback_data: inline.QuestionHomeSquareData):
    await callback.message.answer(
        f"<i>Вы согласны пройти опрос? – Да!\nМестоположение дома? – {decoder.d_city(callback_data.city)}.</i>\n\n"
        f"<b>Сколько квадратных метров планируется быть в вашем доме?</b>",
        parse_mode="HTML", reply_markup=inline.question_home_square(callback_data.city))


@router.callback_query(inline.QuestionBudgetData.filter())
async def question_home_budget(callback: types.CallbackQuery, callback_data: inline.QuestionBudgetData):
    await callback.message.answer(
        f"<i>Вы согласны пройти опрос? – Да!\nМестоположение дома? – {decoder.d_city(callback_data.city)}.\n"
        f"Площадь дома? – {decoder.d_square(callback_data.square)}.</i>\n\n"
        f"<b>Какой вы планируете бюджет?</b>", parse_mode="HTML",
        reply_markup=inline.question_home_budget(callback_data.city, callback_data.square))


@router.callback_query(inline.QuestionFinally.filter())
async def question_home_finally(callback: types.CallbackQuery, callback_data: inline.QuestionFinally):
    city = decoder.d_city(callback_data.city)
    square = decoder.d_square(callback_data.square)
    budget = decoder.d_budget(callback_data.budget)
    await callback.message.answer(
        f"<i>Вы согласны пройти опрос? – Да!\nМестоположение дома? – {city}.\n"
        f"Площадь дома? – {square}."
        f"\nПланируемый бюджет? – {budget}</i>\n\n"
        f"<b>Спасибо за прохождение опроса, наш менеджер скоро с вами свяжется!</b>", parse_mode="HTML")
    db_sqlite3.cur.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?);",
                           (callback.from_user.id, callback_data.city, callback_data.square, callback_data.budget,
                            datetime.datetime.now()))
    db_sqlite3.db.commit()
    for admin in admin_list.list:
        if callback.from_user.username:
            user_link = html.link(callback.from_user.full_name, f"t.me/{callback.from_user.username}")
        else:
            user_link = html.link(callback.from_user.full_name, callback.from_user.url)
        await bot.send_message(admin, f"<b>Новое обращение!</b>"
                                      f"\n\n{user_link}\nID: {callback.from_user.id}"
                                      f"\nМестоположение: {city}."
                                      f"\nПлощадь: {square}."
                                      f"\nБюджет: {budget}."
                                      f"\nВремя обращения: {datetime.datetime.now()}.",
                               parse_mode="HTML")
    await asyncio.sleep(0.5)
    await start(callback.message)
