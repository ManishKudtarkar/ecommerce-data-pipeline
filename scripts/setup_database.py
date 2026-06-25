from pathlib import Path
from sqlalchemy import text
from utils.db import get_engine

def run_sql_file(file_path: str):
    engine = get_engine()
    sql = Path(file_path).read_text(encoding="utf-8")

    with engine.begin() as conn:
        conn.execute(text(sql))

    print(f"Executed SQL file: {file_path}")

if __name__ == "__main__":
    run_sql_file("sql/create_tables.sql")