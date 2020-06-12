import os
from pathlib import Path

import psycopg2

DATABASE_URL = (
    os.getenv("DATABASE_URL") or "postgres://debug:debug@localhost:5432/debug"
)


def connect():
    return psycopg2.connect(DATABASE_URL)


def _get_sql(filename):
    current_dir = Path(__file__).parent
    sql_file = current_dir / filename

    with open(sql_file) as file:
        sql = file.read()
        return sql


def _init_db():
    createdb_sql = _get_sql("createdb.pgsql")
    populate_sql = _get_sql("populate.pgsql")
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(createdb_sql)
            cur.execute(populate_sql)


def _is_db_exists() -> bool:
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT relname "
                "FROM pg_catalog.pg_class "
                "WHERE relname = 'expense'"
            )
            table_exists = cur.fetchall()
            return table_exists


def init_db_if_not_exists():
    if not _is_db_exists():
        _init_db()
