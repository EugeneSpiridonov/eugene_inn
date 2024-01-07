from fastapi import HTTPException
from sqlalchemy import insert, join, select
from sqlalchemy.exc import SQLAlchemyError
from bookings.models import Bookings
from database import async_session_maker
from hotels.rooms.models import Rooms
from logger import logger


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

    @classmethod
    async def add_bulk(cls, *data):
        # Для загрузки массива данных [{"id": 1}, {"id": 2}]
        # мы должны обрабатывать его через позиционные аргументы *args.
        try:
            query = insert(cls.model).values(*data).returning(cls.model.id)
            async with async_session_maker() as session:
                result = await session.execute(query)
                await session.commit()
                return result.mappings().first()
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exc"
            elif isinstance(e, Exception):
                msg = "Unknown Exc"
            msg += ": Cannot bulk insert data into table"

            logger.error(msg, extra={"table": cls.model.__tablename__}, exc_info=True)
            return None
