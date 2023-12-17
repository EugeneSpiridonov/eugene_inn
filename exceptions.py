from fastapi import HTTPException, status


class CustomException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(CustomException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь уже существует"


class IncorrectEmailOrPasswordException(CustomException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверная почта или пароль"


class NotAuthorizedException(CustomException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Вы не авторизованы!"


class TokenExpiredException(CustomException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен истёк или не получен"


class NoTokenException(CustomException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен не получен"


class UserNotFoundException(CustomException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Пользователь не найден"
