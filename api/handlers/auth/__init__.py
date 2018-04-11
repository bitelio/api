from secrets import token_hex
from passlib.context import CryptContext

from api.handlers.base import BaseHandler
from .password import PasswordHandler


class AuthHandler(BaseHandler):
    crypt = CryptContext(schemes="argon2")

    async def post(self):
        query = {"UserName": self.model.UserName.strip().lower(),
                 "Password": {"$exists": True}}
        user = await self.mongo.users.find_one(query)
        if user:
            if self.crypt.verify(self.model.Password, user["Password"]):
                token = token_hex()
                self.redis.set(token, user, ex=self.settings.get("session"))
                self.set_secure_cookie("token", token)
                self.write({"token": token})
            else:
                self.write_error(401, "Wrong password")
        else:
            self.write_error(404, "Wrong username")


routes = {
    "": AuthHandler,
    "password": PasswordHandler,
}
