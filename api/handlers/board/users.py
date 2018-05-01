from api.handlers.base import BaseHandler
from api.mixins import BoardMixin, CollectionMixin


class UsersHandler(BoardMixin, CollectionMixin, BaseHandler):
    collection = "users"
    response = ["Id", "UserName", "FullName", "Role"]
