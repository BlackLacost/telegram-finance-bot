from aiogram import types

import views
from exceptions import NotCorrectMessage
from init_bot import dp
from models import expenses
from models.categories import Categories


@dp.message_handler(commands=["start", "help"])
async def send_help_handler(message: types.Message):
    answer_message = views.send_help()
    await message.answer(answer_message)


@dp.message_handler(commands=["categories"])
async def get_categories_handler(message: types.Message):
    categories = Categories().get_all_categories()
    answer_message = views.get_categories(categories)
    await message.answer(answer_message)


@dp.message_handler(commands=["today"])
async def today_statistics_handler(message: types.Message):
    """Отправляет сегодняшнюю статистику трат"""
    today_expenses = expenses.today_statistics_expenses()
    answer_message = views.today_statistics_expenses(today_expenses)
    await message.answer(answer_message)


@dp.message_handler(commands=["expenses"])
async def list_expenses_handler(message: types.Message):
    last_expenses = expenses.last(10)
    answer_message = views.list_expenses(last_expenses)
    await message.answer(answer_message)


@dp.message_handler(lambda message: message.text.startswith("/del"))
async def del_expense_handler(message: types.Message):
    """Удаляет одну запись о расходе по её идентификатору"""
    expense_id = int(message.text[4:])
    expenses.delete_expense(expense_id)
    answer_message = views.del_expense()
    await message.answer(answer_message)


@dp.message_handler()
async def add_expense_handler(message: types.Message):
    try:
        expense = expenses.add_expense(message.text)
    except NotCorrectMessage as e:
        return await message.answer(str(e))

    today_expenses = expenses.today_statistics_expenses()
    answer_message = views.add_expense(expense, today_expenses)
    await message.answer(answer_message)
