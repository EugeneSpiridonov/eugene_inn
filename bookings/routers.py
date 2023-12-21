from datetime import date
from fastapi import APIRouter, Depends
from pydantic import ValidationError, parse_obj_as
from exceptions import RoomCannotbeBookedException
from tasks.tasks import send_booking_confirmation_email

from users.dependencies import get_current_user
from users.models import Users
from .schema import SBookings

from .dao import BookingsDAO

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"],
)


@router.get("")
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBookings]:
    return await BookingsDAO.find_all(user_id=user.id)


@router.post("", status_code=201, response_model=SBookings)
async def add_booking(
    # background_tasks: BackgroundTasks,
    room_id: int,
    date_from: date,
    date_to: date,
    user: Users = Depends(get_current_user),
):
    booking = await BookingsDAO.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCannotbeBookedException
    try:
        booking_dict = parse_obj_as(SBookings, booking).dict()
    except Exception as e:
        raise ValidationError(f"Ошибка при обработке бронирования: {e}")
    # вариант с celery
    send_booking_confirmation_email.delay(booking_dict, user.email)
    # вариант с background tasks
    # background_tasks.add_task(send_booking_confirmation_email, booking_dict, user.email)
    return booking_dict


@router.delete("/{booking_id}")
async def delete_booking(booking_id: int, user: Users = Depends(get_current_user)):
    await BookingsDAO.delete_my_booking(booking_id=booking_id, user_id=user.id)
