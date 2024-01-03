from typing import List

from pydantic import BaseModel


class SHotels(BaseModel):
    """Валидация полей базы данных"""

    id: int
    name: str
    location: str
    services: List[str]
    rooms_quantity: int
    image_id: int

    class Config:
        # Валидировалось и без этой строки, но всё же:
        from_attributes = True


class SHotelsInfo(SHotels):
    rooms_left: int
