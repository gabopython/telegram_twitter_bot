import aiosqlite


DB_NAME = "bot.db"


async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER,
                username TEXT,
                chat_id INTEGER,
                xp_points INTEGER DEFAULT 0,
                PRIMARY KEY (user_id, chat_id)
            )
        """
        )
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS media (
                chat_id INTEGER,
                file_type TEXT,
                folder TEXT, 
                PRIMARY KEY (chat_id, folder)
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
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS custom_texts (
                chat_id INTEGER PRIMARY KEY,
                custom_text TEXT DEFAULT ''
            )
        """
        )
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS user_reactions (
            user_id INTEGER,
            tweet_id TEXT,
            liked BOOLEAN DEFAULT 0,
            retweeted BOOLEAN DEFAULT 0,
            replied BOOLEAN DEFAULT 0,
            bookmarked BOOLEAN DEFAULT 0,
            smashed BOOLEAN DEFAULT 0,
            PRIMARY KEY (user_id, tweet_id)
            )
        """
        )
        await db.commit()


async def update_custom_text(chat_id: int, custom_text: str):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            """
            INSERT OR REPLACE INTO custom_texts (chat_id, custom_text)
            VALUES (?, ?)
            """,
            (chat_id, custom_text),
        )
        await db.commit()


async def get_custom_text(chat_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            """
            SELECT custom_text FROM custom_texts WHERE chat_id = ?
        """,
            (chat_id,),
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else ""


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


async def add_user(user_id: int, username: str, chat_id: int, xp_points: int = 0):
    async with aiosqlite.connect(DB_NAME) as db:
        # Check if the user already exists in that chat
        async with db.execute(
            "SELECT 1 FROM users WHERE user_id = ? AND chat_id = ?", (user_id, chat_id)
        ) as cursor:
            exists = await cursor.fetchone()

        # Only insert if user does not exist
        if not exists:
            await db.execute(
                """
                INSERT INTO users (user_id, username, chat_id, xp_points)
                VALUES (?, ?, ?, ?)
                """,
                (user_id, username, chat_id, xp_points),
            )
            await db.commit()


async def get_user(user_id: int, chat_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            """
            SELECT user_id, username, chat_id, xp_points FROM users WHERE user_id = ? AND chat_id = ?
            """,
            (user_id, chat_id),
        ) as cursor:
            row = await cursor.fetchone()
            return row if row else None


async def add_xp(user_id: int, chat_id: int, xp_points: int):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            """
            UPDATE users SET xp_points = xp_points + ? WHERE user_id = ? AND chat_id = ?
            """,
            (xp_points, user_id, chat_id),
        )
        await db.commit()


async def has_user_liked_tweet(user_id: int, tweet_id: str) -> bool:
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            """
            SELECT liked FROM user_reactions WHERE user_id = ? AND tweet_id = ?
            """,
            (user_id, tweet_id),
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else False


async def add_user_like(user_id: int, tweet_id: str):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            """
            INSERT OR REPLACE INTO user_reactions (user_id, tweet_id, liked)
            VALUES (?, ?, 1)
            """,
            (user_id, tweet_id),
        )
        await db.commit()


async def has_user_retweeted_tweet(user_id: int, tweet_id: str) -> bool:
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            """
            SELECT retweeted FROM user_reactions WHERE user_id = ? AND tweet_id = ?
            """,
            (user_id, tweet_id),
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else False


async def add_user_retweet(user_id: int, tweet_id: str):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            """
            INSERT OR REPLACE INTO user_reactions (user_id, tweet_id, retweeted)
            VALUES (?, ?, 1)
            """,
            (user_id, tweet_id),
        )
        await db.commit()


async def has_user_replied_tweet(user_id: int, tweet_id: str) -> bool:
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            """
            SELECT replied FROM user_reactions WHERE user_id = ? AND tweet_id = ?
            """,
            (user_id, tweet_id),
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else False


async def add_user_reply(user_id: int, tweet_id: str):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            """
            INSERT OR REPLACE INTO user_reactions (user_id, tweet_id, replied)
            VALUES (?, ?, 1)
            """,
            (user_id, tweet_id),
        )
        await db.commit()


async def has_user_bookmarked_tweet(user_id: int, tweet_id: str) -> bool:
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            """
            SELECT bookmarked FROM user_reactions WHERE user_id = ? AND tweet_id = ?
            """,
            (user_id, tweet_id),
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else False


async def add_user_bookmark(user_id: int, tweet_id: str):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            """
            INSERT OR REPLACE INTO user_reactions (user_id, tweet_id, bookmarked)
            VALUES (?, ?, 1)
            """,
            (user_id, tweet_id),
        )
        await db.commit()


async def has_user_smashed_tweet(user_id: int, tweet_id: str) -> bool:
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            """
            SELECT smashed FROM user_reactions WHERE user_id = ? AND tweet_id = ?
            """,
            (user_id, tweet_id),
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else False


async def add_user_smashed(user_id: int, tweet_id: str):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            """
            INSERT OR REPLACE INTO user_reactions (user_id, tweet_id, smashed)
            VALUES (?, ?, 1)
            """,
            (user_id, tweet_id),
        )
        await db.commit()
