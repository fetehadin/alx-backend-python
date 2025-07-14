#!/usr/bin/env python3
# 1-execute.py

import sqlite3
from typing import Any, Iterable, List, Optional, Tuple


class ExecuteQuery:
    """Context manager that opens a DB connection, runs a single query, and returns its rows."""

    def __init__(self, db_path: str, query: str, params: Iterable[Any] = ()) -> None:
        self.db_path = db_path
        self.query = query
        self.params = tuple(params)
        self.conn: Optional[sqlite3.Connection] = None
        self.rows: List[Tuple[Any, ...]] = []

    def __enter__(self) -> List[Tuple[Any, ...]]:
        self.conn = sqlite3.connect(self.db_path)
        cur = self.conn.cursor()
        cur.execute(self.query, self.params)
        self.rows = cur.fetchall()
        cur.close()
        return self.rows

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        if self.conn:
            if exc_type:
                self.conn.rollback()
            else:
                self.conn.commit()
            self.conn.close()
        return False


if __name__ == "__main__":
    # demo DB and data to ensure table exists
    with sqlite3.connect("demo.db") as seed:
        seed.execute(
            "CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, name TEXT, age INTEGER)"
        )
        if not seed.execute("SELECT COUNT(*) FROM users").fetchone()[0]:
            seed.executemany(
                "INSERT INTO users(name, age) VALUES(?, ?)",
                [("Alice", 30), ("Bob", 20), ("Charlie", 27)],
            )
            seed.commit()

    query = "SELECT * FROM users WHERE age > ?"
    with ExecuteQuery("demo.db", query, (25,)) as result:
        for row in result:
            print(row)
