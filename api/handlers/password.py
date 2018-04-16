from api.handlers import BaseHandler
from api.mixins import PostMixin, TokenMixin
from api.models import PasswordModel, TokenModel


class PasswordHandler(PostMixin, TokenMixin, BaseHandler):
    model = type("PasswordResetModel", (PasswordModel, TokenModel), {})

    async def post(self):
        user = await self.mongo.users.find_one({"Token": self.body.Token})
        if user:
            data = {"Password": self.body.hash(), "Token": None}
            await self.mongo.users.update({"Token": self.body.Token}, data)
            self.write({"token": await self.token()})
        else:
            self.write_error(400)
