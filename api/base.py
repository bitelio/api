from json import loads
from pickle import dumps
from hashlib import sha1
from tornado.web import RequestHandler
from bson.json_util import dumps as jsonify
from cached_property import cached_property
from schematics.exceptions import DataError
from schematics.models import ModelMeta, Model


class BaseHandler(RequestHandler):
    SUPPORTED_METHODS = ["POST", "PUT"]

    def initialize(self):
        self.db = self.settings["db"]
        self.sg = self.settings.get("sg")
        self.log = self.settings["log"]
        self.cache = self.settings["cache"]

    def prepare(self):
        if self.settings.get("authenticate"):
            self.authenticate()
        try:
            method = self.request.method
            self.model = self.schema(self.body, method=method, validate=True)
        except DataError as error:
            self.write_error(400, message=str(error))
            self.log.warning(str(error))

    def authenticate(self):
        token = self.get_secure_cookie("token")
        user = self.cache.get(token)
        if user:
            self.user = loads(user)
            board = self.user["Boards"][0]  # TODO: put boards in cache
            if not board or self.request.method == "PUT" and board["Role"] < 4:
                self.write_error(403, "Forbidden")
        else:
            self.write_error(401, "Unauthorized")

    def write(self, chunk):
        if isinstance(chunk, (dict, list)):
            chunk = jsonify(chunk).encode("utf-8")
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self._write_buffer.append(chunk)

    def write_error(self, status_code=None, message=None, exc_info=None):
        self.set_status(status_code or self._status_code)
        self.write({"error": {"code": status_code, "message": message}})
        self.finish()

    @property
    def body(self) -> str:
        return loads(self.request.body or "{}")

    def _request_summary(self):
        req = self.request
        board_id = getattr(getattr(self, "model", object), "BoardId", "-")
        return f"{req.method} {req.uri} {board_id} {req.remote_ip}"


class MetaModel(ModelMeta):
    def __call__(cls, *args, **kwargs):
        if "method" in kwargs:
            method = kwargs.pop("method")
            mixin = getattr(cls, method, type(method, (object,), {}))
            cls = type(cls.__name__, (mixin, cls), dict(cls.__dict__))
        return type.__call__(cls, *args, **kwargs)


class BaseModel(Model, metaclass=MetaModel):
    class Options:
        serialize_when_none = False

    @cached_property
    def id(self):
        omit = list(self.PUT.__dict__.keys()) if hasattr(self, 'PUT') else []
        data = {key: val for key, val in self._data.items() if key not in omit}
        return sha1(dumps((self.name, data))).hexdigest()


class NotFoundHandler(BaseHandler):
    def prepare(self):
        self.write_error(404, "Invalid URL")
