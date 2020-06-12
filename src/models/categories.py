from dataclasses import dataclass
from typing import List, Union

from models.db import connect


@dataclass
class Category:
    codename: str
    name: str
    is_base_expense: bool


class Categories:
    def __init__(self):
        self._categories = self._load_categories()

    def _load_categories(self) -> List[Category]:
        with connect() as conn, conn.cursor() as cur:
            cur.execute(
                "SELECT codename, name, is_base_expense FROM category"
            )
            categories = [Category(*row) for row in cur]
            return categories

    def get_all_categories(self) -> List[Category]:
        return self._categories

    def get_category(self, category_name: str) -> Union[Category, None]:
        finded = None
        other_category = None
        for category in self._categories:
            if category.codename == "other":
                other_category = category
            if category_name == category.name:
                finded = category
        if not finded:
            finded = other_category
        return finded
