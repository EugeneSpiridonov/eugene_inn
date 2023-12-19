from datetime import date
from fastapi import APIRouter, Depends
from exceptions import RoomCannotbeBookedException

from users.dependencies import get_current_user
from users.models import Users
from .schema import SBookings

from .dao import BookingsDAO

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"],
)


@router.get("")
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBookings]:
    return await BookingsDAO.find_all(user_id=user.id)


@router.post("")
async def add_booking(
    room_id: int,
    date_from: date,
    date_to: date,
    user: Users = Depends(get_current_user),
):
    booking = await BookingsDAO.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCannotbeBookedException


@router.delete("/{booking_id}")
async def delete_booking(booking_id: int, user: Users = Depends(get_current_user)):
    await BookingsDAO.delete_my_booking(booking_id=booking_id, user_id=user.id)
