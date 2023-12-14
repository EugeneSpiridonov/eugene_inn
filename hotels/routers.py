from fastapi import APIRouter
from .schema import SHotels

from .dao import HotelsDAO

router = APIRouter(
    prefix="/hotels",
    tags=["Отели"],
)


@router.get("")
async def get_rooms() -> list[SHotels]:
    return await HotelsDAO.find_all()
