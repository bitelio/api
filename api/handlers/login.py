from api.mixins import PostMixin, TokenMixin
from api.models import UsernameModel, PasswordModel
from api.handlers import BaseHandler


class LoginHandler(PostMixin, TokenMixin, BaseHandler):
    model = type("LoginModel", (UsernameModel, PasswordModel), {})

    async def post(self):
        query = {"UserName": self.body.UserName}
        user = await self.mongo.accounts.find_one(query)
        if user:
            self.log = self.log.bind(user=self.body.UserName)
            if self.body.verify(user["Password"]):
                self.log = self.log.bind(event="Authenticated")
                self.write({"token": await self.token(self.body.UserName)})
            else:
                self.write_error(401, "Wrong password")
        else:
            self.write_error(404, f"Wrong username: {self.body.UserName}")
