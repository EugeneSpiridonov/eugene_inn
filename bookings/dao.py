from dao.base import BaseDAO
from . import models


class BookingsDAO(BaseDAO):
    model = models.Bookings
