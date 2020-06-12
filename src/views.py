from typing import List

from models.expenses import Expense, TodayExpenses
from models.categories import Category


def add_expense(expense: Expense, today_expenses: TodayExpenses) -> str:
    answer_message = (
        f"Добавлены траты {expense.amount} руб на {expense.category_name}.\n\n"
        f"{today_statistics_expenses(today_expenses)}"
    )
    return answer_message


def del_expense() -> str:
    return "Удалил"


def get_categories(categories: List[Category]) -> str:
    answer_message = "Категории трат:\n\n* " + "\n* ".join(
        [category.name for category in categories]
    )
    return answer_message


def list_expenses(expenses: List[Expense]) -> str:
    if not expenses:
        return "Расходы ещё не заведены"

    expenses_rows = [
        f"{expense.amount} руб. на {expense.category_name} - "
        f"нажми /del{expense.id} для удаления"
        for expense in expenses
    ]
    answer_message = "Последние сохранённые траты:\n\n* " + "\n* ".join(
        expenses_rows
    )
    return answer_message


def send_help() -> str:
    answer_message = (
        "Бот для учёта финансов\n\n"
        "Добавить расход: 250 такси\n"
        "Сегодняшняя статистика: /today\n"
        "Последние внесённые расходы: /expenses\n"
        "Категории трат: /categories"
    )
    return answer_message


def today_statistics_expenses(today_expenses: TodayExpenses) -> str:
    if today_expenses.total == 0:
        return "Сегодня ещё нет расходов"
    answer_message = (
        f"Расходы сегодня:\n"
        f"всего - {today_expenses.total} руб.\n"
        f"базовые - {today_expenses.base} руб. из {today_expenses.budget_limit}"
    )
    return answer_message
