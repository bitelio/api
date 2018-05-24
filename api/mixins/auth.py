from json import loads
from tornado.web import Finish


class AuthMixin:
    def prepare(self):
        super().prepare()
        token = self.get_cookie("token")
        user = self.redis.get(f"session:{token}")
        if user:
            self.user = loads(user)
            self.log = self.log.bind(user=self.user["UserName"])
        else:
            self.write_error(401, "Unauthorized")
            raise Finish()
