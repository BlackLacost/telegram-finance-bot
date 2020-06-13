import logging

from aiogram import executor

import handlers
from init_bot import dp
from models.db import init_db_if_not_exists


init_db_if_not_exists()
logging.basicConfig(level=logging.INFO)
executor.start_polling(dp, skip_updates=True)
