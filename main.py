import asyncio
import logging

from aiogram import *

from handlers import admin_private_chat, user_private_chat
from common.config_reader import config

logging.basicConfig(level=logging.INFO)
dp = Dispatcher()
bot = Bot(token=config.bot_token.get_secret_value())

dp.include_routers(admin_private_chat.router, user_private_chat.router)


async def main():
    await bot.get_updates(-1)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
