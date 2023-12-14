from dao.base import BaseDAO
from . import models


class HotelsDAO(BaseDAO):
    model = models.Hotels
