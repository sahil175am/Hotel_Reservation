"""
reservation.py - Reservation class
"""

import uuid
from datetime import date, datetime


class Reservation:
    def __init__(
        self,
        customer_name: str,
        customer_email: str,
        room_number: str,
        check_in: date,
        check_out: date,
        price_per_night: float,
    ):
        if check_out <= check_in:
            raise ValueError("Check-out date must be after check-in date.")
        if check_in < date.today():
            raise ValueError("Check-in date cannot be in the past.")

        self.reservation_id = str(uuid.uuid4())[:8].upper()
        self.customer_name = customer_name
        self.customer_email = customer_email
        self.room_number = room_number
        self.check_in = check_in
        self.check_out = check_out
        self.price_per_night = price_per_night
        self.nights = (check_out - check_in).days
        self.total_price = round(self.nights * price_per_night, 2)
        self.status = "confirmed"   # confirmed | cancelled
        self.created_at = datetime.now().isoformat()

    # ── serialisation ────────────────────────────────────────────────────────

    def to_dict(self):
        return {
            "reservation_id": self.reservation_id,
            "customer_name": self.customer_name,
            "customer_email": self.customer_email,
            "room_number": self.room_number,
            "check_in": self.check_in.isoformat(),
            "check_out": self.check_out.isoformat(),
            "price_per_night": self.price_per_night,
            "nights": self.nights,
            "total_price": self.total_price,
            "status": self.status,
            "created_at": self.created_at,
        }

    @staticmethod
    def from_dict(data: dict):
        r = Reservation.__new__(Reservation)
        r.reservation_id = data["reservation_id"]
        r.customer_name = data["customer_name"]
        r.customer_email = data["customer_email"]
        r.room_number = data["room_number"]
        r.check_in = date.fromisoformat(data["check_in"])
        r.check_out = date.fromisoformat(data["check_out"])
        r.price_per_night = data["price_per_night"]
        r.nights = data["nights"]
        r.total_price = data["total_price"]
        r.status = data["status"]
        r.created_at = data["created_at"]
        return r

    # ── helpers ──────────────────────────────────────────────────────────────

    def overlaps(self, check_in: date, check_out: date) -> bool:
        """Return True if this reservation overlaps with [check_in, check_out)."""
        if self.status == "cancelled":
            return False
        return self.check_in < check_out and self.check_out > check_in

    def __str__(self):
        return (
            f"\n  ┌── Reservation ID : {self.reservation_id}\n"
            f"  │   Guest          : {self.customer_name} <{self.customer_email}>\n"
            f"  │   Room           : {self.room_number}\n"
            f"  │   Check-in       : {self.check_in}\n"
            f"  │   Check-out      : {self.check_out}\n"
            f"  │   Nights         : {self.nights}\n"
            f"  │   Total          : ${self.total_price}\n"
            f"  └── Status         : {self.status.upper()}"
        )
