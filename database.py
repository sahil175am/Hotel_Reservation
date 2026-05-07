"""
database.py - JSON file-based persistence for rooms and reservations
"""

import json
import os
from hotel import Hotel, Room
from reservation import Reservation

ROOMS_FILE = "data/rooms.json"
RESERVATIONS_FILE = "data/reservations.json"


def _ensure_data_dir():
    os.makedirs("data", exist_ok=True)


# ── Rooms ─────────────────────────────────────────────────────────────────────

def save_rooms(hotel: Hotel):
    _ensure_data_dir()
    data = {num: room.to_dict() for num, room in hotel.rooms.items()}
    with open(ROOMS_FILE, "w") as f:
        json.dump(data, f, indent=2)


def load_rooms(hotel: Hotel):
    if not os.path.exists(ROOMS_FILE):
        return
    with open(ROOMS_FILE) as f:
        data = json.load(f)
    for room_data in data.values():
        hotel.rooms[room_data["room_number"]] = Room.from_dict(room_data)


# ── Reservations ──────────────────────────────────────────────────────────────

def save_reservations(reservations: dict[str, Reservation]):
    _ensure_data_dir()
    data = {rid: r.to_dict() for rid, r in reservations.items()}
    with open(RESERVATIONS_FILE, "w") as f:
        json.dump(data, f, indent=2)


def load_reservations() -> dict[str, Reservation]:
    if not os.path.exists(RESERVATIONS_FILE):
        return {}
    with open(RESERVATIONS_FILE) as f:
        data = json.load(f)
    return {rid: Reservation.from_dict(rdata) for rid, rdata in data.items()}
