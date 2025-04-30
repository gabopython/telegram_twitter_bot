import aiosqlite


DB_NAME = "bot.db"


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
                chat_id INTEGER PRIMARY KEY,
                file_type TEXT
            )
        """
        )
        await db.commit()


async def save_image(chat_id: int, file_type: str):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            """
            INSERT OR REPLACE INTO images (chat_id, file_type)
            VALUES (?, ?)
            """,
            (chat_id, file_type),
        )
        await db.commit()


async def get_file_type(chat_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            """
            SELECT file_type FROM images WHERE chat_id = ?
        """,
            (chat_id,),
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else ""


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
