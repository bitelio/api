from json import dumps
from secrets import token_hex

from api.handlers import BaseHandler


class MetaToken(type):
    def __new__(cls, name, bases, body):
        if "Mixin" not in name:
            if BaseHandler not in bases:
                raise TypeError("TokenMixin must inherit from BaseHandler")
        return type.__new__(cls, name, bases, body)


class TokenMixin(metaclass=MetaToken):
    async def token(self, username: str) -> str:
        query = {"UserName": username, "BoardId": {"$exists": True}}
        documents = await self.mongo.users.find(query).to_list(None)
        boards = {doc["BoardId"]: doc["Role"] for doc in documents}
        data = {"UserName": username, "Boards": boards}
        token = token_hex(8)
        duration = self.settings.get("session", 5**5)
        self.redis.set(f"session:{token}", dumps(data), ex=duration)
        self.set_cookie("token", token)
        return token
