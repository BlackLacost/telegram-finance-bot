import os
from pathlib import Path

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from middlewares import AccessMiddleware

load_dotenv(dotenv_path=Path(".") / ".env")

API_TOKEN = os.getenv("API_TOKEN")
PROXY_URL = os.getenv("PROXY_URL")
ACCESS_ID = os.getenv("ACCESS_ID")

bot = Bot(token=API_TOKEN, proxy=PROXY_URL)
dp = Dispatcher(bot)
if ACCESS_ID:
    dp.middleware.setup(AccessMiddleware(int(ACCESS_ID)))
