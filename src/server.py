import logging
import os
from pathlib import Path

from aiogram import Bot, Dispatcher, types, executor
from dotenv import load_dotenv

from exceptions import NotCorrectMessage
from models import expenses
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
async def send_help_handler(message: types.Message):
    await message.answer(
        "Бот для учёта финансов\n\n"
        "Добавить расход: 250 такси\n"
        "Сегодняшняя статистика: /today\n"
        "Последние внесённые расходы: /expenses\n"
        "Категории трат: /categories"
    )


@dp.message_handler(commands=["categories"])
async def get_categories_handler(message: types.Message):
    categories = Categories().get_all_categories()
    answer_message = "Категории трат:\n\n* " + "\n* ".join(
        [category.name for category in categories]
    )
    await message.answer(answer_message)


@dp.message_handler(commands=["today"])
async def today_statistics_handler(message: types.Message):
    """Отправляет сегодняшнюю статистику трат"""
    total_today_expenses = expenses.get_all_today_expenses()
    if total_today_expenses == 0:
        return await message.answer("Сегодня ещё нет расходов")

    base_today_expenses = expenses.get_base_today_expenses()
    budget_limit = expenses.get_budget_limit()

    answer_message = (
        f"Расходы сегодня:\n"
        f"всего - {total_today_expenses} руб.\n"
        f"базовые - {base_today_expenses} руб. из {budget_limit}"
    )
    await message.answer(answer_message)


@dp.message_handler(commands=["expenses"])
async def list_expenses_handler(message: types.Message):
    last_expenses = expenses.last(10)
    if not last_expenses:
        return await message.answer("Расходы ещё не заведены")

    last_expenses_rows = [
        f"{expense.amount} руб. на {expense.category_name} - "
        f"нажми /del{expense.id} для удаления"
        for expense in last_expenses
    ]
    answer_message = "Последние сохранённые траты:\n\n* " + "\n* ".join(
        last_expenses_rows
    )
    await message.answer(answer_message)


@dp.message_handler(lambda message: message.text.startswith("/del"))
async def del_expense_handler(message: types.Message):
    """Удаляет одну запись о расходе по её идентификатору"""
    expense_id = int(message.text[4:])
    expenses.delete_expense(expense_id)
    answer_message = "Удалил"
    await message.answer(answer_message)


@dp.message_handler()
async def add_expense_handler(message: types.Message):
    try:
        expense = expenses.add_expense(message.text)
    except NotCorrectMessage as e:
        return await message.answer(str(e))
    answer_message = (
        f"Добавлены траты {expense.amount} руб на {expense.category_name}"
    )
    await message.answer(answer_message)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
