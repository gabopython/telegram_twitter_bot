import json
from datetime import datetime, timedelta
from collections import deque

class SpotManager:
    def __init__(self, num_spots=5, filename="spots.txt"):
        self.filename = filename
        self.num_spots = num_spots
        self.spots, self.queue = self._load_data()

    # ------------------ PERSISTENCE ------------------ #
    def _load_data(self):
        """Load spots and queue from file."""
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
                spots = data.get("spots", [])
                queue = deque(data.get("queue", []))
                for spot in spots:
                    if spot["expires_at"]:
                        spot["expires_at"] = datetime.fromisoformat(spot["expires_at"])
                return spots, queue
        except (FileNotFoundError, json.JSONDecodeError):
            spots = [
                {"id": i + 1, "taken": False, "user_id": None, "expires_at": None}
                for i in range(self.num_spots)
            ]
            return spots, deque()

    def _save_data(self):
        """Save spots and queue to file."""
        data = {
            "spots": [
                {
                    **spot,
                    "expires_at": spot["expires_at"].isoformat() if spot["expires_at"] else None,
                }
                for spot in self.spots
            ],
            "queue": list(self.queue),
        }
        with open(self.filename, "w") as f:
            json.dump(data, f, indent=2)

    # ------------------ CORE LOGIC ------------------ #
    def _clear_expired(self):
        """Free expired spots and assign from queue if possible."""
        now = datetime.now()
        for spot in self.spots:
            if spot["taken"] and spot["expires_at"] and now > spot["expires_at"]:
                print(f"⏰ Spot {spot['id']} expired (was {spot['user_id']}).")
                spot.update({"taken": False, "user_id": None, "expires_at": None})
        self._assign_from_queue()
        self._save_data()

    def _assign_from_queue(self):
        """Assign waiting users if there are free spots."""
        while self.queue and any(not s["taken"] for s in self.spots):
            user_id, duration = self.queue.popleft()
            self.take_spot(user_id, duration, from_queue=True)

    # ------------------ PUBLIC METHODS ------------------ #
    def take_spot(self, user_id: str, duration_hours: int, from_queue=False):
        """Take a spot or extend user's current one; if full, queue them."""

        # Check if user already has a spot
        for spot in self.spots:
            if spot["taken"] and spot["user_id"] == user_id:
                # User already has a spot
                if not self.queue:  # Queue is empty → extend time
                    spot["expires_at"] += timedelta(hours=duration_hours)
                    self._save_data()
                    print(f"⏱️ Extended time for {user_id} on spot {spot['id']} until {spot['expires_at'].strftime('%H:%M:%S')}")
                    return spot
                else:
                    # Queue not empty → user must wait in queue
                    if not from_queue:
                        self.queue.append((user_id, duration_hours))
                        print(f"🕓 Queue active. {user_id} added to queue (position {len(self.queue)}).")
                        self._save_data()
                    return None

        # Try to assign a new free spot
        for spot in self.spots:
            if not spot["taken"]:
                expires = datetime.now() + timedelta(hours=duration_hours)
                spot.update({"taken": True, "user_id": user_id, "expires_at": expires})
                self._save_data()
                msg = "from queue" if from_queue else "directly"
                print(f"✅ Spot {spot['id']} taken by {user_id} {msg}, until {expires.strftime('%H:%M:%S')}")
                return spot

        # All spots taken → add to queue if not from it
        if not from_queue:
            self.queue.append((user_id, duration_hours))
            print(f"🕓 All spots taken. {user_id} added to waiting queue (position {len(self.queue)}).")
            self._save_data()
        return None


    def status(self):
        """Show current status of spots and queue."""
        self._clear_expired()
        print("\n📊 SPOT STATUS:")
        for spot in self.spots:
            if spot["taken"]:
                exp = spot["expires_at"].strftime("%H:%M:%S")
                print(f"Spot {spot['id']}: TAKEN by {spot['user_id']} until {exp}")
            else:
                print(f"Spot {spot['id']}: AVAILABLE")

        if self.queue:
            print("\n📋 QUEUE:")
            for i, (user, dur) in enumerate(self.queue, 1):
                print(f"{i}. {user} (wants {dur}h)")
        else:
            print("\n📋 Queue is empty.")

# ------------------ EXAMPLE ------------------ #
if __name__ == "__main__":
    manager = SpotManager()
    print()
    manager.take_spot("user1", .05)
    manager.take_spot("user2", .05)  # Should go to queue
    manager.take_spot("user1", .15)
    manager.take_spot("user3", .1)
    manager.take_spot("user4", .15)
    manager.take_spot("user5", .15)
    manager.take_spot("user2", .15)  # Should extend time
    manager.take_spot("user3", .15)  # Should go to queue
    manager.take_spot("user6", .1)   # Should go to queue
    manager.take_spot("user7", .1)  # Should go to queue
    manager.take_spot("user8", .05)   # Should go to queue
    manager.take_spot("user4", .1)  # Should go to queue
    print()
    manager.status()
    print()
