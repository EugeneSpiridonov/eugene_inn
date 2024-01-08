from datetime import date
import json
import pika
from fastapi import APIRouter, Depends, BackgroundTasks
from fastapi_versioning import version
from pydantic import ValidationError, parse_obj_as

from exceptions import RoomCannotbeBookedException
from tasks.tasks import send_booking_confirmation_email
from users.dependencies import get_current_user
from users.models import Users

from .dao import BookingsDAO
from .schema import SBookings

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"],
)


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()
        return super().default(obj)


# Устанавливаем соединение с RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

# Создаем очереди
channel.queue_declare(queue="new_bookings", durable=True)
channel.queue_declare(queue="process_bookings", durable=True)
channel.queue_declare(queue="notify_users", durable=True)


def publish_message(queue_name, message):
    channel.basic_publish(
        exchange="",
        routing_key=queue_name,
        body=json.dumps(message),  # Не используем DateTimeEncoder
        properties=pika.BasicProperties(delivery_mode=2),
    )


@router.get("")
@version(1)
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBookings]:
    return await BookingsDAO.find_all(user_id=user.id)


@router.post("", status_code=201, response_model=SBookings)
@version(1)
async def add_booking(
    background_tasks: BackgroundTasks,
    room_id: int,
    date_from: date,
    date_to: date,
    user: Users = Depends(get_current_user),
):
    # Создаем бронирование
    booking = await BookingsDAO.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCannotbeBookedException

    try:
        booking_dict = parse_obj_as(SBookings, booking).dict()
        print(booking_dict)
    except Exception as e:
        raise ValidationError(f"Ошибка при обработке бронирования: {e}")

    # Отправляем бронирование в очередь для обработки
    publish_message(
        "new_bookings",
        {"Пользователь": booking_dict["user_id"], "Комната": booking_dict["room_id"]},
    )

    # Отправляем уведомление в очередь для пользователей
    background_tasks.add_task(
        publish_message,
        "notify_users",
        json.dumps({"user_id": user.id, "message": "Ваш заказ обработан."}),
    )

    return booking_dict


# Обработчик для очереди новых бронирований
def process_booking(
    ch, method, properties, body, user: Users = Depends(get_current_user)
):
    booking_dict = json.loads(body)
    send_booking_confirmation_email.delay(booking_dict, user.email)
    ch.basic_ack(delivery_tag=method.delivery_tag)


@router.delete("/{booking_id}")
@version(1)
async def delete_booking(booking_id: int, user: Users = Depends(get_current_user)):
    await BookingsDAO.delete_my_booking(booking_id=booking_id, user_id=user.id)


# Указываем функцию обработки для очереди 'new_bookings'
channel.basic_consume(
    queue="new_bookings", on_message_callback=process_booking, auto_ack=False
)

# Запускаем обработку сообщений в фоне
import threading

threading.Thread(target=channel.start_consuming).start()
