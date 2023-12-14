from dao.base import BaseDAO
from . import models


class RoomsDAO(BaseDAO):
    model = models.Rooms
