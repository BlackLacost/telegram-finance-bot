import logging

from aiogram import executor

import controllers
from init_bot import dp
from models.db import init_db_if_not_exists


logging.basicConfig(level=logging.INFO)

init_db_if_not_exists()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
