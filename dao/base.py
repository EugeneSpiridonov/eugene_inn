from fastapi import HTTPException
from sqlalchemy import insert, select, join
from database import async_session_maker
from bookings.models import Bookings
from rooms.models import Rooms


class BaseDAO:
    """Методы для работы с БД"""

    model = None

    @classmethod
    async def find_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            # .__table__.columns избавляет от лишней вложенности
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def find_user_bookrooms(cls, user_id: int):
        # Получаем бронирования и комнаты конкретного пользователя
        async with async_session_maker() as session:
            # .__table__.columns избавляет от лишней вложенности
            query = (
                select(
                    Bookings.__table__.columns,
                    Rooms.__table__.columns,
                )
                .join(Rooms, Rooms.id == Bookings.room_id, isouter=True)
                .where(Bookings.user_id == user_id)
            )

            result = await session.execute(query)
            return result.mappings().all()

    # @classmethod
    # async def add(cls, **data):
    #     async with async_session_maker() as session:
    #         query = insert(cls.model).values(**data).returning(cls.model.id)
    #         await session.execute(query)
    #         await session.commit()

    @classmethod
    async def add(cls, **data):
        try:
            async with async_session_maker.begin() as session:
                query = insert(cls.model).values(**data).returning(cls.model.id)
                await session.execute(query)
        except Exception as e:
            # Обработка ошибок и откат транзакции
            return HTTPException(status_code=500)
