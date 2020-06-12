import logging
import os
from pathlib import Path

from aiogram import Bot, Dispatcher, types, executor
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(".") / ".env")

API_TOKEN = os.getenv("API_TOKEN")
PROXY_URL = os.getenv("PROXY_URL")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN, proxy=PROXY_URL)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start", "help"])
async def send_help(message: types.Message):
    await message.answer("Бот для учёта финансов")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
