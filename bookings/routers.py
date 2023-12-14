from fastapi import APIRouter
from .schema import SBookings

from .dao import BookingsDAO

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"],
)


@router.get("")
async def get_bookings() -> list[SBookings]:
    return await BookingsDAO.find_all()
