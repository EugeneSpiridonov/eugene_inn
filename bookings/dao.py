from datetime import date
from sqlalchemy import delete, insert, select, func, and_, or_
from database import async_session_maker, engine
from dao.base import BaseDAO
from .schema import SBookings
from hotels.models import Hotels
from rooms.models import Rooms
from .models import Bookings


class BookingsDAO(BaseDAO):
    model = Bookings

    @classmethod
    async def add(cls, user_id: int, room_id: int, date_from: date, date_to: date):
        """
        WITH booked_rooms AS (
        SELECT * FROM bookings
        WHERE room_id = 1 AND
        (date_from >= '2023-05-15' AND date_from <= '2023-06-20') OR
        (date_from <= '2023-05-15' AND date_from > '2023-05-15')
        )
        SELECT rooms.quantity - COUNT(booked_rooms.room_id) FROM rooms
        LEFT JOIN booked_rooms ON booked_rooms_room_id = rooms.id
        WHERE rooms.id = 1
        GROUP BY rooms.quantity, booked_rooms.room_id
        """
        async with async_session_maker() as session:
            booked_rooms = (
                select(Bookings).where(
                    and_(
                        Bookings.room_id == 1,
                        or_(
                            and_(
                                Bookings.date_from >= date_from,
                                Bookings.date_from <= date_to,
                            ),
                            and_(
                                Bookings.date_from <= date_from,
                                Bookings.date_to > date_from,
                            ),
                        ),
                    )
                )
            ).cte("booked_rooms")

            rooms_left = (
                select(
                    (Rooms.quantity - func.count(booked_rooms.c.room_id)).label(
                        "rooms_left"
                    )
                )
                .select_from(Rooms)
                .join(booked_rooms, booked_rooms.c.room_id == Rooms.id)
                .where(Rooms.id == room_id)
                .group_by(Rooms.quantity, booked_rooms.c.room_id)
            )

            # Вывести этот запрос на экран
            # print(rooms_left.compile(engine, compile_kwargs={"literal_binds": True}))
            rooms_left = await session.execute(rooms_left)
            print(rooms_left.scalar())
            """
            WITH booked_rooms AS
            (SELECT bookings.id AS id, bookings.room_id AS room_id, bookings.user_id AS user_id, bookings.date_from AS date_from, bookings.date_to AS date_to, bookings.price AS price, bookings.total_days AS total_days, bookings.total_cost AS total_cost
            FROM bookings WHERE bookings.room_id = 1 AND (bookings.date_from >= '2023-05-15' AND bookings.date_from <= '2023-06-20' OR bookings.date_from <= '2023-05-15' AND bookings.date_to > '2023-05-15'))
            SELECT rooms.quantity - count(booked_rooms.room_id) AS rooms_left
            FROM rooms JOIN booked_rooms ON booked_rooms.room_id = rooms.id
            WHERE rooms.id = 1 GROUP BY rooms.quantity, booked_rooms.room_id
            """
