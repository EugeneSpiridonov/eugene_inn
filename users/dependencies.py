from datetime import datetime

from fastapi import Depends, Request
from jose import JWTError, jwt

from config import settings
from exceptions import (
    NotAuthorizedException,
    NoTokenException,
    TokenExpiredException,
    UserNotFoundException,
)
from users.dao import UsersDAO


def get_token(request: Request):
    token = request.cookies.get("booking_access_token")
    if not token:
        raise NotAuthorizedException
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        # Получаем токен
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
    except JWTError:
        raise NoTokenException
    # Проверяем, не истёк ли токен
    expire: str = payload.get("exp")
    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise TokenExpiredException
    # Получаем user.id
    user_id: str = payload.get("sub")
    if not user_id:
        raise UserNotFoundException
    user = await UsersDAO.find_by_id(int(user_id))
    if not user:
        raise UserNotFoundException
    return user
