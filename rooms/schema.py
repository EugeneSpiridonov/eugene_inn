from typing import List
from pydantic import BaseModel


class SRooms(BaseModel):
    """Валидация полей базы данных"""

    id: int
    hotel_id: int
    name: str
    description: str
    price: int
    services: List[str]
    quantity: int
    image_id: int

    class Config:
        # Валидировалось и без этой строки, но всё же:
        from_attributes = True
