from secrets import token_hex
from schematics.types import StringType
from passlib.context import CryptContext

from api import route
from api.base import BaseHandler, BaseModel


class AuthModel(BaseModel):
    UserName = StringType(required=True)
    Password = StringType(required=True)

    @property
    def query(self):
        return {"UserName": self.UserName.strip().lower(),
                "Password": {"$exists": True}}


@route
class AuthHandler(BaseHandler):
    # TODO: update user from cache when changed on kanban
    # TODO: remove open sessions when changing password
    crypt = CryptContext(schemes="argon2")

    def authenticate(self):
        pass

    async def post(self):
        user = await self.db.users.find_one(self.model.query)
        if user:
            if self.crypt.verify(self.model.Password, user["Password"]):
                token = token_hex()
                self.cache.set(token, user, ex=self.settings.get("session"))
                self.set_secure_cookie("token", token)
                self.write({"token": token})
            else:
                self.write_error(401, "Wrong password")
        else:
            self.write_error(404, "Wrong username")
