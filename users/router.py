from fastapi import APIRouter, HTTPException
from users.auth import get_password_hash
from users.dao import UsersDAO

from users.schema import SUserRegister

router = APIRouter(
    prefix="/auth",
    tags=["Аутентификация и пользователи"],
)


@router.post("/register")
async def register_user(user_data: SUserRegister):
    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise HTTPException(status_code=500, detail="Такой пользователь уже существует")
    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.add(email=user_data.email, hashed_password=hashed_password)
    return {"message": "Пользователь создан!"}
