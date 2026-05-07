"""
hotel.py - Room and Hotel classes
"""

ROOM_TYPES = {
    "single":  {"beds": 1, "price": 80,  "capacity": 1},
    "double":  {"beds": 2, "price": 120, "capacity": 2},
    "suite":   {"beds": 2, "price": 250, "capacity": 4},
    "deluxe":  {"beds": 3, "price": 350, "capacity": 6},
}


class Room:
    def __init__(self, room_number: str, room_type: str, floor: int):
        if room_type not in ROOM_TYPES:
            raise ValueError(f"Invalid room type. Choose from: {list(ROOM_TYPES.keys())}")
        self.room_number = room_number
        self.room_type = room_type
        self.floor = floor
        self.price_per_night = ROOM_TYPES[room_type]["price"]
        self.capacity = ROOM_TYPES[room_type]["capacity"]
        self.beds = ROOM_TYPES[room_type]["beds"]

    def to_dict(self):
        return {
            "room_number": self.room_number,
            "room_type": self.room_type,
            "floor": self.floor,
            "price_per_night": self.price_per_night,
            "capacity": self.capacity,
            "beds": self.beds,
        }

    @staticmethod
    def from_dict(data: dict):
        r = Room(data["room_number"], data["room_type"], data["floor"])
        return r

    def __str__(self):
        return (f"Room {self.room_number} | {self.room_type.title()} | "
                f"Floor {self.floor} | ${self.price_per_night}/night | "
                f"{self.beds} bed(s) | capacity: {self.capacity}")


class Hotel:
    def __init__(self, name: str):
        self.name = name
        self.rooms: dict[str, Room] = {}

    def add_room(self, room: Room):
        if room.room_number in self.rooms:
            raise ValueError(f"Room {room.room_number} already exists.")
        self.rooms[room.room_number] = room
        print(f"  ✔ Room {room.room_number} ({room.room_type}) added.")

    def get_room(self, room_number: str) -> Room | None:
        return self.rooms.get(room_number)

    def list_rooms(self):
        return list(self.rooms.values())

    def seed_default_rooms(self):
        """Pre-populate the hotel with sample rooms."""
        default_rooms = [
            ("101", "single", 1), ("102", "single", 1),
            ("103", "double", 1), ("104", "double", 1),
            ("201", "double", 2), ("202", "double", 2),
            ("203", "suite",  2), ("204", "suite",  2),
            ("301", "suite",  3), ("302", "deluxe", 3),
            ("303", "deluxe", 3),
        ]
        print(f"\n  Setting up {self.name} with {len(default_rooms)} rooms...")
        for num, rtype, floor in default_rooms:
            self.add_room(Room(num, rtype, floor))
