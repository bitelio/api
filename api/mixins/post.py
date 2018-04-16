from json import loads
from tornado.web import Finish
from schematics.exceptions import DataError


class PostMixin:
    def prepare(self):
        super().prepare()
        try:
            self.body = self.model(loads(self.request.body), validate=True)
        except DataError as error:
            self.write_error(400, str(error))
            raise Finish()
