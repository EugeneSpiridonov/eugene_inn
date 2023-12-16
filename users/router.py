from fastapi import APIRouter, HTTPException, Response, status
from users.auth import authentificate_user, create_access_token, get_password_hash
from users.dao import UsersDAO
from users.schema import SUserAuth

router = APIRouter(
    prefix="/auth",
    tags=["Аутентификация и пользователи"],
)


@router.post("/register")
async def register_user(user_data: SUserAuth):
    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise HTTPException(status_code=500, detail="Такой пользователь уже существует")
    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.add(email=user_data.email, hashed_password=hashed_password)
    return {"message": "Пользователь создан!"}


@router.post("/login")
async def login_user(response: Response, user_data: SUserAuth):
    user = await authentificate_user(user_data.email, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Неправильные данные"
        )
    access_token = create_access_token({"sub": user.id})
    response.set_cookie("booking_access_token", access_token, httponly=True)
    return {"access_token": access_token}
