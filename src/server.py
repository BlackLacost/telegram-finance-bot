import logging
import os
from pathlib import Path

from aiogram import Bot, Dispatcher, types, executor
from dotenv import load_dotenv

from models.categories import Categories
from models.db import init_db_if_not_exists
from middlewares import AccessMiddleware

load_dotenv(dotenv_path=Path(".") / ".env")

API_TOKEN = os.getenv("API_TOKEN")
PROXY_URL = os.getenv("PROXY_URL")
ACCESS_ID = os.getenv("ACCESS_ID")

logging.basicConfig(level=logging.INFO)

init_db_if_not_exists()

bot = Bot(token=API_TOKEN, proxy=PROXY_URL)
dp = Dispatcher(bot)
if ACCESS_ID:
    dp.middleware.setup(AccessMiddleware(int(ACCESS_ID)))


@dp.message_handler(commands=["start", "help"])
async def send_help(message: types.Message):
    await message.answer(
        "Бот для учёта финансов\n\n" "Категории трат: /categories"
    )


@dp.message_handler(commands=["categories"])
async def categories_list(message: types.Message):
    categories = Categories().get_all_categories()
    answer_message = "Категории трат:\n\n* " + "\n* ".join(
        [category.name for category in categories]
    )
    await message.answer(answer_message)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
