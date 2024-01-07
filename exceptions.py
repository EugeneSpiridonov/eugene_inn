from fastapi import HTTPException, status


class CustomException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


# Пользовательские исключения
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


# Исключения по бронированиям
class RoomCannotbeBookedException(CustomException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Не осталось свободных номеров"


class TooLongBookingException(CustomException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Max period booking is 30 days"


class BackToTheFutureException(CustomException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Date_to must be later than date_from"


# Общие
class NotFound(CustomException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Not found"


class UserNotEnoughPermissions(CustomException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Not enough permissions"


class CannotAddDataToDatabase(CustomException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Не удалось добавить запись"


class CannotProcessCSV(CustomException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Не удалось обработать CSV файл"
