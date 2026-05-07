"""
main.py - Hotel Reservation System
Entry point: handles the menu and all user interactions.
"""

from datetime import date

from hotel import Hotel, Room, ROOM_TYPES
from reservation import Reservation
import database as db
from utils import (
    get_date, get_non_empty, get_choice,
    print_header, print_divider, availability_grid,
)

HOTEL_NAME = "Grand Python Hotel"


# ─────────────────────────────────────────────────────────────────────────────
# Feature functions
# ─────────────────────────────────────────────────────────────────────────────

def book_room(hotel: Hotel, reservations: dict):
    print_header("Book a Room")

    # 1. Collect dates first so we can show live availability
    check_in = get_date("  Check-in  date (YYYY-MM-DD): ")
    check_out = get_date("  Check-out date (YYYY-MM-DD): ")
    if check_out <= check_in:
        print("  ✖ Check-out must be after check-in.")
        return
    if check_in < date.today():
        print("  ✖ Check-in date cannot be in the past.")
        return

    # 2. Show available rooms for those dates
    availability_grid(hotel.list_rooms(), reservations, check_in, check_out)

    # 3. Let customer pick a room
    room_number = get_non_empty("\n  Enter room number to book (or 0 to cancel): ")
    if room_number == "0":
        return

    room = hotel.get_room(room_number)
    if room is None:
        print(f"  ✖ Room {room_number} does not exist.")
        return

    # 4. Check availability
    conflict = any(
        r.room_number == room_number and r.overlaps(check_in, check_out)
        for r in reservations.values()
    )
    if conflict:
        print(f"  ✖ Room {room_number} is not available for those dates.")
        return

    # 5. Customer details
    name  = get_non_empty("  Guest name  : ")
    email = get_non_empty("  Guest email : ")

    # 6. Confirm
    nights = (check_out - check_in).days
    total  = nights * room.price_per_night
    print(f"\n  Summary:")
    print(f"    Room  : {room}")
    print(f"    Dates : {check_in} → {check_out}  ({nights} nights)")
    print(f"    Total : ${total:.2f}")
    confirm = get_choice("\n  Confirm booking? (yes/no): ", ["yes", "no"])
    if confirm == "no":
        print("  Booking cancelled.")
        return

    # 7. Create & save
    res = Reservation(name, email, room_number, check_in, check_out, room.price_per_night)
    reservations[res.reservation_id] = res
    db.save_reservations(reservations)
    print(f"\n  ✔ Booking confirmed!")
    print(res)


def check_availability(hotel: Hotel, reservations: dict):
    print_header("Check Room Availability")
    check_in  = get_date("  From date (YYYY-MM-DD): ")
    check_out = get_date("  To   date (YYYY-MM-DD): ")
    if check_out <= check_in:
        print("  ✖ Check-out must be after check-in.")
        return
    availability_grid(hotel.list_rooms(), reservations, check_in, check_out)


def view_reservation(reservations: dict):
    print_header("View Reservation")
    rid = get_non_empty("  Enter Reservation ID: ").upper()
    res = reservations.get(rid)
    if res is None:
        print(f"  ✖ No reservation found with ID: {rid}")
        return
    print(res)


def cancel_reservation(reservations: dict):
    print_header("Cancel Reservation")
    rid = get_non_empty("  Enter Reservation ID to cancel: ").upper()
    res = reservations.get(rid)
    if res is None:
        print(f"  ✖ No reservation found with ID: {rid}")
        return
    if res.status == "cancelled":
        print("  ✖ This reservation is already cancelled.")
        return
    print(res)
    confirm = get_choice("\n  Are you sure you want to cancel? (yes/no): ", ["yes", "no"])
    if confirm == "yes":
        res.status = "cancelled"
        db.save_reservations(reservations)
        print(f"  ✔ Reservation {rid} cancelled.")
    else:
        print("  Cancellation aborted.")


def list_all_reservations(reservations: dict):
    print_header("All Reservations")
    active = [r for r in reservations.values() if r.status == "confirmed"]
    cancelled = [r for r in reservations.values() if r.status == "cancelled"]
    print(f"  Confirmed: {len(active)}   Cancelled: {len(cancelled)}")
    print_divider()
    if not reservations:
        print("  No reservations found.")
        return
    for res in sorted(reservations.values(), key=lambda r: r.check_in):
        print(res)


def add_room_menu(hotel: Hotel):
    print_header("Add a New Room")
    room_number = get_non_empty("  Room number (e.g. 401): ")
    if hotel.get_room(room_number):
        print(f"  ✖ Room {room_number} already exists.")
        return
    print(f"  Available types: {', '.join(ROOM_TYPES.keys())}")
    room_type = get_choice("  Room type: ", list(ROOM_TYPES.keys()))
    try:
        floor = int(get_non_empty("  Floor number: "))
    except ValueError:
        print("  ✖ Floor must be a number.")
        return
    hotel.add_room(Room(room_number, room_type, floor))
    db.save_rooms(hotel)
    print(f"  ✔ Room saved.")


def list_rooms_menu(hotel: Hotel):
    print_header("All Rooms")
    rooms = sorted(hotel.list_rooms(), key=lambda r: r.room_number)
    if not rooms:
        print("  No rooms configured.")
        return
    for room in rooms:
        print(f"  {room}")


# ─────────────────────────────────────────────────────────────────────────────
# Main menu
# ─────────────────────────────────────────────────────────────────────────────

MENU = """
  ╔══════════════════════════════════════════╗
  ║       HOTEL SAHIL PALACE  🏨             ║
  ╠══════════════════════════════════════════╣
  ║  1. Book a room                          ║
  ║  2. Check availability                   ║
  ║  3. View a reservation                   ║
  ║  4. Cancel a reservation                 ║
  ║  5. List all reservations                ║
  ║  6. List all rooms                       ║
  ║  7. Add a room  (admin)                  ║
  ║  0. Exit                                 ║
  ╚══════════════════════════════════════════╝
"""

def main():
    hotel = Hotel(HOTEL_NAME)

    # Load existing data; seed rooms on first run
    db.load_rooms(hotel)
    if not hotel.rooms:
        hotel.seed_default_rooms()
        db.save_rooms(hotel)

    reservations = db.load_reservations()

    print(f"\n  Welcome to {HOTEL_NAME}!")

    while True:
        print(MENU)
        choice = input("  Enter your choice: ").strip()

        if   choice == "1": book_room(hotel, reservations)
        elif choice == "2": check_availability(hotel, reservations)
        elif choice == "3": view_reservation(reservations)
        elif choice == "4": cancel_reservation(reservations)
        elif choice == "5": list_all_reservations(reservations)
        elif choice == "6": list_rooms_menu(hotel)
        elif choice == "7": add_room_menu(hotel)
        elif choice == "0":
            print("\n  Goodbye! 👋\n")
            break
        else:
            print("  ✖ Invalid choice. Please enter 0–7.")


if __name__ == "__main__":
    main()
