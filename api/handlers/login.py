from api.mixins import PostMixin, TokenMixin
from api.models import UsernameModel, PasswordModel
from api.handlers import BaseHandler


class LoginHandler(PostMixin, TokenMixin, BaseHandler):
    model = type("LoginModel", (UsernameModel, PasswordModel), {})

    async def post(self):
        query = {"UserName": self.body.UserName, "Password": {"$exists": True}}
        user = await self.mongo.users.find_one(query)
        if user:
            self.log = self.log.bind(user=self.body.UserName)
            if self.model.verify():
                self.write({"token": await self.token()})
            else:
                self.write_error(401, "Wrong password")
        else:
            self.write_error(404, f"Wrong username: {self.body.UserName}")
