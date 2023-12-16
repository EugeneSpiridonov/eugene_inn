from fastapi import APIRouter, Depends, Request

from users.dependencies import get_current_user
from users.models import Users
from .schema import SBookings

from .dao import BookingsDAO

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"],
)


@router.get("")
async def get_bookings(user: Users = Depends(get_current_user)):  # -> list[SBookings]:
    return await BookingsDAO.find_all(user_id=1)
