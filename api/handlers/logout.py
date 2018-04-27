from api.mixins import AuthMixin
from api.handlers import BaseHandler


class LogoutHandler(AuthMixin, BaseHandler):
    def get(self):
        token = self.get_cookie("token")
        status = self.redis.delete(f"session:{token}")
        self.write({"message": status})
