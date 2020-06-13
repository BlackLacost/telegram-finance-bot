import re
import datetime
from dataclasses import dataclass
from typing import List, Optional

import pytz

from exceptions import NotCorrectMessage
from models.categories import Categories
from models.db import connect


@dataclass
class Message:
    amount: int
    category_text: str


@dataclass
class ExpensesStats:
    total: int
    base: int
    budget_limit: int


@dataclass
class Expense:
    id: Optional[int]
    amount: int
    category_name: str


def add_expense(raw_message: str) -> Expense:
    parsed_message = _parse_message(raw_message)
    category = Categories().get_category(parsed_message.category_text)

    with connect() as conn, conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO expense(amount, created, category_codename, raw_text)
            VALUES (%s, NOW(), %s, %s)
            """,
            (
                parsed_message.amount,
                category.codename,
                parsed_message.category_text,
            ),
        )
    return Expense(
        id=None, amount=parsed_message.amount, category_name=category.name
    )


def delete_expense(expense_id: int) -> None:
    with connect() as conn, conn.cursor() as cur:
        cur.execute(
            "DELETE FROM expense WHERE id = %s", (expense_id,),
        )


def _get_all_today_expenses() -> int:
    """Возвращает все сегодняшние расходы"""
    with connect() as conn, conn.cursor() as cur:
        cur.execute(
            """
            SELECT SUM(amount)
            FROM expense
            WHERE DATE(created)=DATE('NOW')
            """
        )
        result = cur.fetchone()
        total_expenses = result[0] if result[0] else 0
        return total_expenses


def _get_base_today_expenses() -> int:
    """Возвращает базовые расходы на сегодня"""
    with connect() as conn, conn.cursor() as cur:
        cur.execute(
            """
            SELECT SUM(amount)
            FROM expense
            WHERE
                DATE(created)=DATE('NOW')
                AND category_codename IN (
                    SELECT codename
                    FROM category
                    WHERE is_base_expense=true
                )
            """
        )
        result = cur.fetchone()
        base_today_expenses = result[0] if result[0] else 0
        return base_today_expenses


def _get_budget_limit() -> int:
    """Возвращает дневной лимит трат для основных базовых трат"""
    with connect() as conn, conn.cursor() as cur:
        cur.execute("SELECT daily_limit FROM budget WHERE codename = 'base'")
        base_limit = int(cur.fetchone()[0])
        return base_limit


def today_statistics_expenses() -> ExpensesStats:
    return ExpensesStats(
        total=_get_all_today_expenses(),
        base=_get_base_today_expenses(),
        budget_limit=_get_budget_limit(),
    )


def _get_total_month_expenses() -> int:
    """Возвращает сумму расходов за текущий месяц"""
    first_day_of_month = _get_first_day_of_month()
    with connect() as conn, conn.cursor() as cur:
        cur.execute(
            """
            SELECT SUM(amount)
            FROM expense
            WHERE DATE(created) >= %s
            """,
            (first_day_of_month,),
        )
        result = cur.fetchone()
        total_month_expenses = result[0] if result[0] else 0
        return total_month_expenses


def _get_total_base_month_expenses() -> int:
    """Возвращает сумму базовых расходов за текущей месяц"""
    first_day_of_month = _get_first_day_of_month()
    with connect() as conn, conn.cursor() as cur:
        cur.execute(
            """
            SELECT SUM(amount)
            FROM expense
            WHERE
                DATE(created) >= %s
                AND category_codename IN (
                    SELECT codename
                    FROM category
                    WHERE is_base_expense=true
                )
            """,
            (first_day_of_month,),
        )
        result = cur.fetchone()
        total_base_month_expenses = result[0] if result[0] else 0
        return total_base_month_expenses


def month_statistics_expenses() -> ExpensesStats:
    now = _get_now_datetime()
    return ExpensesStats(
        total=_get_total_month_expenses(),
        base=_get_total_base_month_expenses(),
        budget_limit=now.day * _get_budget_limit(),
    )


def last(num: int) -> List[Expense]:
    """Возвращает последние несколько расходов"""
    with connect() as conn, conn.cursor() as cur:
        cur.execute(
            """
            SELECT
                expense.id,
                expense.amount,
                category.name
            FROM expense
            JOIN category
                ON expense.category_codename = category.codename
            ORDER BY created DESC
            LIMIT %s
            """,
            (num,),
        )
        last_expenses = [Expense(*row) for row in cur]
        return last_expenses


def _parse_message(raw_message: str) -> Message:
    regexp_result = re.match(r"([\d]+) (.*)", raw_message)
    if (
        not regexp_result
        or not regexp_result.group(0)
        or not regexp_result.group(1)
        or not regexp_result.group(2)
    ):
        raise NotCorrectMessage(
            "Не могу понять сообщение. Напишите сообщение в формате, "
            "например:\n1500 метро"
        )
    amount = int(regexp_result.group(1))
    category_text = regexp_result.group(2).strip().lower()
    return Message(amount=amount, category_text=category_text)


def _get_now_datetime() -> datetime.datetime:
    """Возвращает сегодняшний datetime с учётом времненной зоны Мск."""
    tz = pytz.timezone("Europe/Moscow")
    now = datetime.datetime.now(tz)
    return now


def _get_now_formatted() -> str:
    """Возвращает сегодняшнюю дату строкой"""
    return _get_now_datetime().strftime("%Y-%m-%d %H:%M:%S")


def _get_first_day_of_month() -> str:
    now = _get_now_datetime()
    first_day_of_month = f"{now.year:04d}-{now.month:02d}-01"
    return first_day_of_month
