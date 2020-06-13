from dataclasses import dataclass
from typing import List, Union

from models.db import connect


@dataclass
class Category:
    codename: str
    name: str
    is_base_expense: bool
    aliases: List[str]


class Categories:
    def __init__(self):
        self._categories = self._load_categories()

    def _load_categories(self) -> List[Category]:
        with connect() as conn, conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    codename,
                    name,
                    is_base_expense,
                    aliases
                FROM category
                """
            )
            categories = [
                Category(
                    codename=codename,
                    name=name,
                    is_base_expense=is_base_expense,
                    aliases=self._fill_aliases(aliases, codename, name),
                )
                for (codename, name, is_base_expense, aliases) in cur
            ]
            return categories

    def _fill_aliases(
        self, aliases: str, codename: str, name: str
    ) -> List[str]:
        result = aliases.split(",")
        result = list(filter(None, map(str.strip, result)))
        result.append(codename)
        result.append(name)
        return result

    def get_all_categories(self) -> List[Category]:
        return self._categories

    def get_category(self, category_name: str) -> Union[Category, None]:
        finded = None
        other_category = None
        for category in self._categories:
            if category.codename == "other":
                other_category = category
            for alias in category.aliases:
                if category_name in alias:
                    finded = category
        if not finded:
            finded = other_category
        return finded
