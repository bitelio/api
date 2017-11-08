from json import loads
from bson.json_util import dumps
from tornado.web import RequestHandler
from schematics.exceptions import DataError

from api import models


class BaseHandler(RequestHandler):
    SUPPORTED_METHODS = ["POST", "PUT"]

    def initialize(self):
        self.db = self.settings["db"]
        self.log = self.settings["log"]
        self.cache = self.settings["cache"]

    def prepare(self):
        try:
            method = self.request.method
            self.model = self.schema(self.body, method=method, validate=True)
        except DataError as error:
            self.write_error(400, message=str(error))
            self.log.warning(str(error))

    def write(self, chunk):
        if isinstance(chunk, (dict, list)):
            chunk = dumps(chunk).encode("utf-8")
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self._write_buffer.append(chunk)

    def write_error(self, status_code=None, message=None, exc_info=None):
        self.set_status(status_code or self._status_code)
        self.write({"error": {"code": status_code, "message": message}})
        self.finish()

    @property
    def body(self):
        return loads(self.request.body or "{}")

    @property
    def schema(self):
        name = self.__class__.__name__[:-7]
        module = getattr(models, name.lower())
        return getattr(module, f"{name}Model")


class NotFoundHandler(BaseHandler):
    def prepare(self):
        self.write_error(404, "Invalid URL")
