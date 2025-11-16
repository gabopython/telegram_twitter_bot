import aiosqlite
from datetime import datetime, timedelta
from collections import deque
import asyncio

class SpotManager:
    def __init__(self, num_spots=5, db_name="spots.db"):
        self.db_name = db_name
        self.num_spots = num_spots

    # ------------------ INIT ------------------ #
    async def init_db(self):
        """Initialize database and tables."""
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS spots (
                    id INTEGER PRIMARY KEY,
                    taken INTEGER,
                    user_id TEXT,
                    expires_at TEXT
                )
            """)
            await db.execute("""
                CREATE TABLE IF NOT EXISTS queue (
                    position INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    duration_hours REAL,
                    spot INTEGER
                )
            """)
            await db.commit()

            async with db.execute("SELECT COUNT(*) FROM spots") as cursor:
                count = (await cursor.fetchone())[0]
                if count == 0:
                    for i in range(self.num_spots):
                        await db.execute(
                            "INSERT INTO spots (id, taken, user_id, expires_at) VALUES (?, 0, NULL, NULL)",
                            (i + 1,)
                        )
                    await db.commit()

    # ------------------ DB HELPERS ------------------ #
    async def _get_spots(self):
        async with aiosqlite.connect(self.db_name) as db:
            cursor = await db.execute("SELECT id, taken, user_id, expires_at FROM spots")
            rows = await cursor.fetchall()
            return [
                {
                    "id": r[0],
                    "taken": bool(r[1]),
                    "user_id": r[2],
                    "expires_at": datetime.fromisoformat(r[3]) if r[3] else None
                }
                for r in rows
            ]

    async def _save_spot(self, spot):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute("""
                UPDATE spots SET taken=?, user_id=?, expires_at=? WHERE id=?
            """, (
                int(spot["taken"]),
                spot["user_id"],
                spot["expires_at"].isoformat() if spot["expires_at"] else None,
                spot["id"]
            ))
            await db.commit()

    async def _get_queue(self):
        async with aiosqlite.connect(self.db_name) as db:
            cursor = await db.execute("SELECT user_id, duration_hours, spot FROM queue ORDER BY position ASC")
            rows = await cursor.fetchall()
            return deque(rows)

    async def _save_queue(self, queue):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute("DELETE FROM queue")
            for user_id, duration, spot in queue:
                await db.execute("INSERT INTO queue (user_id, duration_hours, spot) VALUES (?, ?, ?)", (user_id, duration, spot))
            await db.commit()

    # ------------------ CORE LOGIC ------------------ #
    async def _clear_expired(self):
        """Free expired spots and assign from queue if possible."""
        spots = await self._get_spots()
        queue = await self._get_queue()
        now = datetime.now()

        for spot in spots:
            if spot["taken"] and spot["expires_at"] and now > spot["expires_at"]:
                print(f"⏰ Spot {spot['id']} expired (was {spot['user_id']}).")
                spot.update({"taken": False, "user_id": None, "expires_at": None})
                await self._save_spot(spot)

        return await self._assign_from_queue()

    async def _assign_from_queue(self):
        """Assign waiting users if there are free spots."""
        queue = await self._get_queue()
        if queue:
            user_id, duration, spot = queue.popleft()
            await self._save_queue(queue)
            return await self.take_spot(user_id, duration, spot)

    # ------------------ PUBLIC METHODS ------------------ #
    async def take_spot(self, user_id: str, duration_hours: float, spot_id: int = None):
        """Take a spot or extend user's current one; if full, queue them."""
        spots = await self._get_spots()
        queue = await self._get_queue()

        if spot_id:
            # Assign specific spot from queue
            expires = datetime.now() + timedelta(hours=duration_hours)         
            s= {"taken": True, "user_id": user_id, "expires_at": expires, "id": spot_id}
            await self._save_spot(s)
            print(f"✅ Spot {s['id']} taken by {user_id} from queue, until {expires.strftime('%H:%M:%S')}")
            return s

        # Check if user already has a spot
        for spot in spots:
            if spot["taken"] and spot["user_id"] == user_id:
                if not queue:  # Extend time if no one waiting
                    spot["expires_at"] += timedelta(hours=duration_hours)
                    await self._save_spot(spot)
                    print(f"⏱️ Extended time for {user_id} on spot {spot['id']} until {spot['expires_at'].strftime('%H:%M:%S')}")
                    return spot

        # Try to assign a new free spot
        for spot in spots:
            if not spot["taken"]:
                expires = datetime.now() + timedelta(hours=duration_hours)
                spot.update({"taken": True, "user_id": user_id, "expires_at": expires})
                await self._save_spot(spot)
                print(f"✅ Spot {spot['id']} taken by {user_id}, until {expires.strftime('%H:%M:%S')}")
                return spot

        # All spots taken → add to queue if not from it
        if spot_id is None:
            # get the spot with the earliest expiry
            earliest_spot = min(spots, key=lambda s: s["expires_at"])

            queue.append((user_id, duration_hours, earliest_spot["id"]))
            await self._save_queue(queue)
            time_assigned = earliest_spot["expires_at"].strftime('%H:%M:%S')
            earliest_spot["expires_at"]+= timedelta(hours=duration_hours)
            await self._save_spot(earliest_spot)
            return f"🕓 All spots taken. {user_id} will be queued in spot {earliest_spot['id']}, {time_assigned}."

    async def status(self, spot_id: int = None):
        """Show current status of spots and queue."""
        s = await self._clear_expired()
        if s is not None:
            return s
        spots = await self._get_spots()
        queue = await self._get_queue()

        print("\n📊 SPOT STATUS:")
        for spot in spots:
            if spot["taken"]:
                print(f"Spot {spot['id']}: TAKEN by {spot['user_id']}")
                if spot_id and spot["id"] == spot_id:
                    return False               
            else:
                print(f"Spot {spot['id']}: AVAILABLE")

        if queue:
            print("\n📋 QUEUE:")
            for i, (user, dur, spot) in enumerate(queue, 1):
                print(f"{i}. {user} (wants {dur}h)")
        else:
            print("\n📋 Queue is empty.")

# ------------------ EXAMPLE ------------------ #
async def main():
    manager = SpotManager()
    # await manager.init_db()
    # await manager.take_spot("user1", .15)
    # await manager.take_spot("user2", .05)
    # await manager.take_spot("user3", .1)
    # await manager.take_spot("user4", .15)
    # await manager.take_spot("user5", .15)
    # await manager.take_spot("user3", .15)
    # await manager.take_spot("user9", .1)
    # await manager.take_spot("user7", .1)
    # await manager.take_spot("user8", .05)
    # await manager.take_spot("user4", .1)

    print()
    await manager.status()
    print()

if __name__ == "__main__":
    asyncio.run(main())
