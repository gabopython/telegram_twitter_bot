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
                chat_id INTEGER,
                file_type TEXT
            )
        """
        )
        await db.commit()


async def save_image(chat_id: int, file_type: str):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            """
            INSERT INTO images (chat_id, file_type) VALUES (?, ?)
        """,
            (chat_id, file_type),
        )
        await db.commit()


async def update_file_type(chat_id: int, new_file_type: str):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            """
            UPDATE images
            SET file_type = ?
            WHERE chat_id = ?
        """,
            (new_file_type, chat_id),
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
            return row[0] if row else None


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
