from datetime import date

from sqlalchemy import and_, delete, func, insert, or_, select

from dao.base import BaseDAO
from database import async_session_maker
from exceptions import NotFound, UserNotEnoughPermissions
from hotels.rooms.models import Rooms

from .models import Bookings
from .schema import SBookings


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
                        Bookings.room_id == room_id,
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

            get_rooms_left = (
                select(
                    (Rooms.quantity - func.count(booked_rooms.c.room_id)).label(
                        "rooms_left"
                    )
                )
                .select_from(Rooms)
                .join(booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True)
                .where(Rooms.id == room_id)
                .group_by(Rooms.quantity, booked_rooms.c.room_id)
            )

            # Вывести этот запрос на экран
            # print(get_rooms_left.compile(engine, compile_kwargs={"literal_binds": True}))

            """
            WITH booked_rooms AS
            (SELECT bookings.id AS id, bookings.room_id AS room_id, bookings.user_id AS user_id, bookings.date_from AS date_from, bookings.date_to AS date_to, bookings.price AS price, bookings.total_days AS total_days, bookings.total_cost AS total_cost
            FROM bookings WHERE bookings.room_id = 1 AND (bookings.date_from >= '2023-05-15' AND bookings.date_from <= '2023-06-20' OR bookings.date_from <= '2023-05-15' AND bookings.date_to > '2023-05-15'))
            SELECT rooms.quantity - count(booked_rooms.room_id) AS rooms_left
            FROM rooms LEFT JOIN booked_rooms ON booked_rooms.room_id = rooms.id
            WHERE rooms.id = 1 GROUP BY rooms.quantity, booked_rooms.room_id
            """
            rooms_left = await session.execute(get_rooms_left)
            rooms_left: int = rooms_left.scalar()

            if not rooms_left or rooms_left > 0:
                get_price = select(Rooms.price).filter_by(id=room_id)
                price = await session.execute(get_price)
                price: int = price.scalar()
                add_booking = (
                    insert(Bookings)
                    .values(
                        room_id=room_id,
                        user_id=user_id,
                        date_from=date_from,
                        date_to=date_to,
                        price=price,
                    )
                    .returning(Bookings)
                )
                new_booking = await session.execute(add_booking)
                await session.commit()
                return new_booking.scalar()
            else:
                return None

    @classmethod
    async def delete_my_booking(cls, booking_id: int, user_id: int):
        async with async_session_maker() as session:
            get_user_id_by_booking_id = (
                select(Bookings.user_id)
                .select_from(Bookings)
                .where(Bookings.id == booking_id)
            )

            user_id_by_booking_id = await session.execute(get_user_id_by_booking_id)
            user_id_by_booking_id: int = user_id_by_booking_id.scalar()

            if user_id_by_booking_id is None:
                raise NotFound

            if user_id_by_booking_id != user_id:
                raise UserNotEnoughPermissions

            delete_booking_by_id = delete(Bookings).where(Bookings.id == booking_id)

            result = await session.execute(delete_booking_by_id)
            await session.commit()

            return result
