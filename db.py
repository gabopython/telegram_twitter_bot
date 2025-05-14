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
            CREATE TABLE IF NOT EXISTS media (
                chat_id INTEGER PRIMARY KEY,
                file_type TEXT,
                folder TEXT
            )
        """
        )
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS default_targets (
                chat_id INTEGER PRIMARY KEY,
                likes_default_target INTEGER DEFAULT 10,
                retweets_default_target INTEGER DEFAULT 3,
                replies_default_target INTEGER DEFAULT 5,
                views_default_target INTEGER DEFAULT 0,
                bookmarks_default_target INTEGER DEFAULT 0
            )
        """
        )
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS targets (
                chat_id INTEGER PRIMARY KEY,
                likes_target INTEGER DEFAULT 10,
                retweets_target INTEGER DEFAULT 3,
                replies_target INTEGER DEFAULT 5,
                views_target INTEGER DEFAULT 0,
                bookmarks_target INTEGER DEFAULT 0
            )
        """
        )
        await db.commit()


async def update_likes_default_target(chat_id: int, likes_default_target: int):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            """
            INSERT OR REPLACE INTO default_targets (chat_id, likes_default_target)
            VALUES (?, ?)
            """,
            (chat_id, likes_default_target),
        )
        await db.commit()


async def update_retweets_default_target(chat_id: int, retweets_default_target: int):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            """
            INSERT OR REPLACE INTO default_targets (chat_id, retweets_default_target)
            VALUES (?, ?)
            """,
            (chat_id, retweets_default_target),
        )
        await db.commit()


async def update_replies_default_target(chat_id: int, replies_default_target: int):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            """
            INSERT OR REPLACE INTO default_targets (chat_id, replies_default_target)
            VALUES (?, ?)
            """,
            (chat_id, replies_default_target),
        )
        await db.commit()


async def update_views_default_target(chat_id: int, views_default_target: int):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            """
            INSERT OR REPLACE INTO default_targets (chat_id, views_default_target)
            VALUES (?, ?)
            """,
            (chat_id, views_default_target),
        )
        await db.commit()


async def update_bookmarks_default_target(chat_id: int, bookmarks_default_target: int):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            """
            INSERT OR REPLACE INTO default_targets (chat_id, bookmarks_default_target)
            VALUES (?, ?)
            """,
            (chat_id, bookmarks_default_target),
        )
        await db.commit()


async def update_likes_target(chat_id: int, likes_target: int):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            """
            INSERT OR REPLACE INTO targets (chat_id, likes_target)
            VALUES (?, ?)
            """,
            (chat_id, likes_target),
        )
        await db.commit()


async def update_retweets_target(chat_id: int, retweets_target: int):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            """
            INSERT OR REPLACE INTO targets (chat_id, retweets_target)
            VALUES (?, ?)
            """,
            (chat_id, retweets_target),
        )
        await db.commit()


async def update_replies_target(chat_id: int, replies_target: int):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            """
            INSERT OR REPLACE INTO targets (chat_id, replies_target)
            VALUES (?, ?)
            """,
            (chat_id, replies_target),
        )
        await db.commit()


async def update_views_target(chat_id: int, views_target: int):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            """
            INSERT OR REPLACE INTO targets (chat_id, views_target)
            VALUES (?, ?)
            """,
            (chat_id, views_target),
        )
        await db.commit()


async def update_bookmarks_target(chat_id: int, bookmarks_target: int):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            """
            INSERT OR REPLACE INTO targets (chat_id, bookmarks_target)
            VALUES (?, ?)
            """,
            (chat_id, bookmarks_target),
        )
        await db.commit()


async def get_likes_default_target(chat_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            """
            SELECT likes_default_target FROM default_targets WHERE chat_id = ?
        """,
            (chat_id,),
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else 10


async def get_retweets_default_target(chat_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            """
            SELECT retweets_default_target FROM default_targets WHERE chat_id = ?
        """,
            (chat_id,),
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else 3


async def get_replies_default_target(chat_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            """
            SELECT replies_default_target FROM default_targets WHERE chat_id = ?
        """,
            (chat_id,),
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else 5


async def get_views_default_target(chat_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            """
            SELECT views_default_target FROM default_targets WHERE chat_id = ?
        """,
            (chat_id,),
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else 0


async def get_bookmarks_default_target(chat_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            """
            SELECT bookmarks_default_target FROM default_targets WHERE chat_id = ?
        """,
            (chat_id,),
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else 0


async def get_likes_target(chat_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            """
            SELECT likes_target FROM targets WHERE chat_id = ?
        """,
            (chat_id,),
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else 10


async def get_retweets_target(chat_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            """
            SELECT retweets_target FROM targets WHERE chat_id = ?
        """,
            (chat_id,),
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else 3


async def get_replies_target(chat_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            """
            SELECT replies_target FROM targets WHERE chat_id = ?
        """,
            (chat_id,),
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else 5


async def get_views_target(chat_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            """
            SELECT views_target FROM targets WHERE chat_id = ?
        """,
            (chat_id,),
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else 0


async def get_bookmarks_target(chat_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            """
            SELECT bookmarks_target FROM targets WHERE chat_id = ?
        """,
            (chat_id,),
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else 0


async def get_file_type(chat_id: int, folder: str):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            """
            SELECT file_type FROM media WHERE chat_id = ? AND folder = ?
        """,
            (chat_id, folder),
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else ""


async def save_media(chat_id: int, file_type: str, folder: str):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            """
            INSERT OR REPLACE INTO media (chat_id, file_type, folder)
            VALUES (?, ?, ?)
            """,
            (chat_id, file_type, folder),
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
