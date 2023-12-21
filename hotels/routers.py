import asyncio
from fastapi_cache.decorator import cache
from datetime import date, timedelta, datetime
from fastapi import APIRouter, Query

from exceptions import BackToTheFutureException, NotFound, TooLongBookingException
from .schema import SHotels, SHotelsInfo

from .dao import HotelsDAO

router = APIRouter(
    prefix="/hotels",
    tags=["Отели"],
)


# @router.get("")
# async def get_hotels() -> list[SHotels]:
#     return await HotelsDAO.find_all()


@router.get("", response_model=list[SHotelsInfo])
@cache(expire=20)  # Кэшируем результат запроса в Redis
async def get_hotels_by_location_and_time(
    location: str = Query(..., description=f"Например, Алтай"),
    date_from: date = Query(..., description=f"Например, {datetime.now().date()}"),
    date_to: date = Query(..., description=f"Например, {datetime.now().date()}"),
):
    # await asyncio.sleep(3)
    if date_from > date_to:
        raise TooLongBookingException
    if date_to - date_from > timedelta(days=30):
        raise BackToTheFutureException
    return await HotelsDAO.find_all(location, date_from, date_to)


@router.get("/id/{hotel_id}", response_model=SHotels)
async def get_hotel_info(hotel_id: int):
    result = await HotelsDAO.find_one_or_none(id=hotel_id)
    if result:
        return result
    raise NotFound
