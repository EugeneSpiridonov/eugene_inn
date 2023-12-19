from fastapi import APIRouter, Depends, Response
from exceptions import IncorrectEmailOrPasswordException, UserAlreadyExistsException
from users.auth import authentificate_user, create_access_token, get_password_hash
from users.dao import UsersDAO
from users.dependencies import get_current_user
from users.models import Users
from users.schema import SUsers, SUserAuth

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


# Регистрация и аутентификация
auth_router = APIRouter(
    prefix="/auth",
    tags=["Аутентификация и пользователи"],
)


@auth_router.post("/register")
async def register_user(user_data: SUserAuth):
    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.add(email=user_data.email, hashed_password=hashed_password)
    return {"message": "Пользователь создан!"}


@auth_router.post("/login")
async def login_user(response: Response, user_data: SUserAuth):
    user = await authentificate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("booking_access_token", access_token, httponly=True)
    return {"access_token": access_token}


@auth_router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("booking_access_token")
    return {"message": "Пользователь вышел из системы"}


@auth_router.get("/me")
async def get_my_info(current_user: Users = Depends(get_current_user)):
    return current_user
