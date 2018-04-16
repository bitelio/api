from api.mixins import PostMixin
from api.models import UserModel
from api.handlers import BaseHandler


class UserHandler(PostMixin, BaseHandler):
    model = UserModel

    def get(self):
        pass

    def post(self):
        pass
