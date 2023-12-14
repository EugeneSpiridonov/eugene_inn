from fastapi import APIRouter
from .schema import SRooms

from .dao import RoomsDAO

router = APIRouter(
    prefix="/rooms",
    tags=["Комнаты"],
)


@router.get("")
async def get_rooms() -> list[SRooms]:
    return await RoomsDAO.find_all()
