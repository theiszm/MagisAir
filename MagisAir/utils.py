from pathlib import Path
from django.db import connection


def load_sql_file(path_to_sql: str):
    """ Loads and executes SQL statements in an .sql file including INSERT/UPDATE/DELETE """
    sql_path = Path(path_to_sql)

    if not sql_path.exists():
        raise FileNotFoundError(f"SQL file not found: {path_to_sql}")

    sql = sql_path.read_text(encoding="utf-8")

    with connection.cursor() as cursor:
        statements = sql.split(";")
        for stmt in statements:
            stmt = stmt.strip()
            if stmt:
                cursor.execute(stmt)
