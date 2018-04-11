from json import loads


class AuthMixin:
    def prepare(self):
        token = self.get_cookie("token")
        user = self.redis.get(token)
        if user:
            self.user = loads(user)
            self.log = self.log.bind(user=self.user["UserName"])
            super().prepare()
        else:
            self.write_error(401, "Unauthorized")
