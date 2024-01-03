from datetime import date

from fastapi import APIRouter

from .dao import RoomsDAO
from .schema import SRooms

router = APIRouter(
    prefix="/rooms",
    tags=["Комнаты"],
)


@router.get("")
async def get_all_rooms() -> list[SRooms]:
    return await RoomsDAO.find_all()


@router.get("/{hotel_id}/rooms", response_model=list[SRooms])
async def get_rooms(
    hotel_id: int,
    date_from: date,
    date_to: date,
):
    return await RoomsDAO.find_all_rooms_in_hotel(hotel_id, date_from, date_to)
