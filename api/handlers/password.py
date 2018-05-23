from api.handlers import BaseHandler
from api.mixins import PostMixin, TokenMixin
from api.models import PasswordModel, TokenModel


class PasswordHandler(PostMixin, TokenMixin, BaseHandler):
    model = type("PasswordResetModel", (PasswordModel, TokenModel), {})

    async def post(self):
        user = await self.mongo.users.find_one({"Token": self.body.Token})
        if user:
            self.log = self.log.bind(event="Resetting password")
            user.update({"Password": self.body.hash(), "Token": None})
            await self.mongo.users.update({"Token": self.body.Token}, user)
            self.write({"token": await self.token(user["UserName"])})
        else:
            self.write_error(400, "Invalid token")
