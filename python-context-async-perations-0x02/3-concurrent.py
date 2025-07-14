#!/usr/bin/env python3
# 2-async_queries.py

import asyncio
import aiosqlite
from typing import List, Tuple

DB_PATH = "demo.db"


async def async_fetch_users() -> List[Tuple[int, str, int]]:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            return await cursor.fetchall()


async def async_fetch_older_users() -> List[Tuple[int, str, int]]:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            return await cursor.fetchall()


async def fetch_concurrently() -> None:
    all_users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users(),
    )
    print("All users:", all_users)
    print("Users > 40:", older_users)


if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
