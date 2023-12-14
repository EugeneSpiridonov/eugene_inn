from pydantic import BaseModel


class SUsers(BaseModel):
    """Валидация полей базы данных"""

    id: int
    email: str
    hashed_password: str

    class Config:
        # Валидировалось и без этой строки, но всё же:
        from_attributes = True
