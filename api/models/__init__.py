from pickle import dumps
from hashlib import sha1
from schematics.models import ModelMeta, Model


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

    @property
    def hash(self):
        pickle = dumps((self.__class__.__name__, dict(self._data)))
        return sha1(pickle).hexdigest()
