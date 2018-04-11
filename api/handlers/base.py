from bson.json_util import dumps
from tornado.web import RequestHandler


class BaseHandler(RequestHandler):
    SUPPORTED_METHODS = ["GET", "POST"]

    def initialize(self):
        self.sg = self.settings.get("sg")
        self.log = self.settings["log"]
        self.redis = self.settings["redis"]
        self.mongo = self.settings["mongo"]

    def write(self, chunk):
        if isinstance(chunk, (dict, list)):
            chunk = dumps(chunk).encode("utf-8")
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self._write_buffer.append(chunk)

    def write_error(self, status_code=None, message=None, exc_info=None):
        self.set_status(status_code or self._status_code)
        self.write({"error": {"code": status_code, "message": message}})
        self.finish()

    @classmethod
    def name(cls):
        return cls.__module__.split("handlers")[-1].replace(".", "/")
