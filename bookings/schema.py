from datetime import date
from pydantic import BaseModel


class SBookings(BaseModel):
    """Валидация полей базы данных"""

    id: int
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int
    total_days: int
    total_cost: int

    class Config:
        # Валидировалось и без этой строки, но всё же:
        from_attributes = True