from dao.base import BaseDAO

from . import models


class UsersDAO(BaseDAO):
    model = models.Users
