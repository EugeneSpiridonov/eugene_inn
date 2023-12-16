from fastapi import APIRouter
from .schema import SUsers

from .dao import UsersDAO

router = APIRouter(
    prefix="/users",
    tags=["Пользователи"],
)


@router.get("")
async def get_users() -> list[SUsers]:
    return await UsersDAO.find_all()


@router.get("/{id}/bookings")
async def get_users_bookings(id: int):
    return await UsersDAO.find_user_bookrooms(id)
