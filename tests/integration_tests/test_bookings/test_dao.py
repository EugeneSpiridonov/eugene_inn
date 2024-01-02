from bookings.dao import BookingsDAO
from datetime import datetime


async def test_add_and_get_booking():
    new_booking = await BookingsDAO.add(
        user_id=2,
        room_id=2,
        date_from=datetime.strptime("2023-07-10", "%Y-%m-%d"),
        date_to=datetime.strptime("2023-07-24", "%Y-%m-%d"),
    )
    assert new_booking.room_id == 2
