from pydantic import BaseModel
from typing import List


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
