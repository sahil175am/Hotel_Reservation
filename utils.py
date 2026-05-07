"""
utils.py - Input helpers and display utilities
"""

from datetime import date


def get_date(prompt: str) -> date:
    """Ask the user for a date in YYYY-MM-DD format, retry on error."""
    while True:
        raw = input(prompt).strip()
        try:
            return date.fromisoformat(raw)
        except ValueError:
            print("  ✖ Invalid format. Please use YYYY-MM-DD (e.g. 2025-12-25).")


def get_non_empty(prompt: str) -> str:
    while True:
        val = input(prompt).strip()
        if val:
            return val
        print("  ✖ This field cannot be empty.")


def get_choice(prompt: str, valid: list[str]) -> str:
    while True:
        val = input(prompt).strip().lower()
        if val in valid:
            return val
        print(f"  ✖ Please enter one of: {', '.join(valid)}")


def print_header(title: str):
    width = 52
    print("\n" + "═" * width)
    print(f"  {title}")
    print("═" * width)


def print_divider():
    print("─" * 52)


def availability_grid(rooms, reservations: dict, check_in: date, check_out: date):
    """Print a simple availability table for a date range."""
    print_header(f"Availability  {check_in} → {check_out}")
    print(f"  {'Room':<8} {'Type':<10} {'Floor':<7} {'Price/Night':<14} {'Status'}")
    print_divider()
    for room in sorted(rooms, key=lambda r: r.room_number):
        booked = any(
            r.room_number == room.room_number and r.overlaps(check_in, check_out)
            for r in reservations.values()
        )
        status = "✖ BOOKED" if booked else "✔ FREE"
        print(f"  {room.room_number:<8} {room.room_type:<10} {room.floor:<7} "
              f"${room.price_per_night:<13} {status}")
