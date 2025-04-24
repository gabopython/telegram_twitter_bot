import aiosqlite


DB_NAME = "users.db"


async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT
            )
        """
        )
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS images (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                file_path TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """
        )
        await db.commit()


async def save_image(user_id: int, file_path: str):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            """
            INSERT INTO images (user_id, file_path) VALUES (?, ?)
        """,
            (user_id, file_path),
        )
        await db.commit()


# async def add_user(user_id: int, username: str):
#     async with aiosqlite.connect(DB_NAME) as db:
#         await db.execute(
#             """
#             INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)
#         """,
#             (user_id, username),
#         )
#         await db.commit()


# async def get_users():
#     async with aiosqlite.connect(DB_NAME) as db:
#         async with db.execute("SELECT * FROM users") as cursor:
#             return await cursor.fetchall()
