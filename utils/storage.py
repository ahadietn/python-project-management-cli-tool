"""Save and load all data as a single JSON file."""

import json
import os
from models.user import User

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "data.json")


def save(users: list[User]):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    try:
        with open(DATA_FILE, "w") as f:
            json.dump({"users": [u.to_dict() for u in users]}, f, indent=2)
    except OSError as e:
        print(f"[ERROR] Could not save: {e}")


def load() -> list[User]:
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE) as f:
            data = json.load(f)
        return [User.from_dict(u) for u in data.get("users", [])]
    except (json.JSONDecodeError, OSError) as e:
        print(f"[WARNING] Could not load data: {e}")
        return []