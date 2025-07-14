#!/usr/bin/env python3

import sqlite3
from typing import Optional


class DatabaseConnection:
    def __init__(self, db_path: str) -> None:
        self.db_path: str = db_path
        self.conn: Optional[sqlite3.Connection] = None
        self.cursor: Optional[sqlite3.Cursor] = None

    def __enter__(self) -> sqlite3.Cursor:
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        if self.cursor is not None:
            self.cursor.close()
        if self.conn is not None:
            if exc_type:
                self.conn.rollback()
            else:
                self.conn.commit()
            self.conn.close()
        return False


if __name__ == "__main__":
    with sqlite3.connect("demo.db") as seed_conn:
        seed_conn.execute(
            "CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, name TEXT)"
        )
        rows = seed_conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        if rows == 0:
            seed_conn.executemany(
                "INSERT INTO users(name) VALUES(?)",
                [("Alice",), ("Bob",), ("Charlie",)],
            )
            seed_conn.commit()

    with DatabaseConnection("demo.db") as cur:
        cur.execute("SELECT * FROM users")
        for row in cur.fetchall():
            print(row)

