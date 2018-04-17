from json import loads
from tornado.web import Finish
from schematics.exceptions import DataError


class PostMixin:
    def prepare(self):
        super().prepare()
        if self.request.method == "POST":
            try:
                body = loads(self.request.body or "{}")
                self.body = self.model(body, validate=True)
            except DataError as error:
                self.write_error(400, str(error))
                raise Finish()
