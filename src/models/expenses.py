import re
from dataclasses import dataclass
from typing import Optional

from exceptions import NotCorrectMessage
from models.categories import Categories
from models.db import connect


@dataclass
class Message:
    amount: int
    category_text: str


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
