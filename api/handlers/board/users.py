from api.handlers.base import BaseHandler
from api.mixins import AuthMixin, BoardMixin, CollectionMixin


class UsersHandler(AuthMixin, BoardMixin, CollectionMixin, BaseHandler):
    collection = "users"
    response = ["Id", "UserName", "FullName", "Role"]
