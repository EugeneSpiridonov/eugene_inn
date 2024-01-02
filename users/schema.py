from pydantic import BaseModel, EmailStr, validator


class SUsers(BaseModel):
    """Валидация полей базы данных"""

    id: int
    email: EmailStr
    hashed_password: str

    class Config:
        # Валидировалось и без этой строки, но всё же:
        from_attributes = True


class SUserAuth(BaseModel):
    """Валидация данных пользователя при регистрации"""

    email: EmailStr
    password: str

    @validator("email")
    def validate_email(cls, value):
        # Проверка, что в строке нет кириллических символов
        if any(
            char.isalpha() and char >= "\u0400" and char <= "\u04FF" for char in value
        ):
            raise ValueError("Email не должен содержать кириллицу")
        return value
