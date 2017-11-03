from json import dumps, loads
from logging import getLogger
from tornado.web import RequestHandler
from schematics.models import ModelMeta, Model
from schematics.exceptions import DataError

from api import cache, handlers


class BaseHandler(RequestHandler):
    SUPPORTED_METHODS = ["POST", "PUT"]

    def initialize(self):
        self.db = self.settings["db"]

    def prepare(self):
        try:
            method = self.request.method
            self.model = self.schema(self.body, method=method, validate=True)
        except DataError as error:
            self.write_error(400, message=str(error))
            self.log.warning(str(error))
        # if self.model in cache:
            # self.write(cache.get(self.model))

    def write(self, chunk):
        response = dumps(chunk).replace("</", "<\\/").encode("utf-8")
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self._write_buffer.append(response)

    def write_error(self, status_code=None, message=None, exc_info=None):
        self.set_status(status_code or self._status_code)
        self.write({"error": {"code": status_code, "message": message}})
        self.finish()

    @property
    def body(self):
        return loads(self.request.body or "{}")

    @property
    def log(self):
        return getLogger(f"{self.__module__}.{self.__class__.__name__}")

    @property
    def schema(self):
        name = self.__class__.__name__[:-7]
        module = getattr(handlers, name.lower())
        return getattr(module, f"{name}Model")


class NotFoundHandler(BaseHandler):
    def prepare(self):
        self.write_error(404, "Invalid URL")


class MetaModel(ModelMeta):
    def __call__(cls, *args, **kwargs):
        if "method" in kwargs:
            method = kwargs.pop("method")
            mixin = getattr(cls, method, type(method, (object,), {}))
            name = f"{cls.__name__} ({mixin.__name__})"
            cls = type(name, (mixin, cls), dict(cls.__dict__))
        return type.__call__(cls, *args, **kwargs)


class BaseModel(Model, metaclass=MetaModel):
    class Options:
        serialize_when_none = False
