__author__ = "Guillermo Guirao Aguilar"
__email__ = "info@bitelio.com"
__version__ = "0.0.1"


from re import match
from os import path, listdir
from importlib import import_module
from tornado import options
from tornado.web import Application

from api.base import NotFoundHandler


def route(handler):
    name = handler.__name__[:-7]
    module = import_module(handler.__module__)
    url = f"/{name.lower()}"
    parent = handler.__bases__[0]
    while parent.__name__ is not "BaseHandler":
        url = f"/{parent.__name__.lower()[:-7]}" + url
        parent = parent.__bases__[0]
    routes.append((f"/api{url}", handler))
    handler.schema = getattr(module, f"{name}Model")
    return handler


def start(env):
    modules = ["auth", "user", "board"]
    dirname = path.dirname(__file__)
    for module in modules:
        import_module(f"api.{module}")
        for filename in listdir(path.join(dirname, module)):
            if match("[a-z]+.py", filename):
                feature = filename[:-3]
                import_module(f"api.{module}.{feature}")

    options.parse_config_file(f"api/config/{env}.py")
    return Application(routes, default_handler_class=NotFoundHandler,
                       **options.options.group_dict("application"))


options.define("db", group="application", type=object)
options.define("log", group="application", type=object)
options.define("cache", group="application", type=object)
options.define("debug", group="application", type=bool)
options.define("session", group="application", type=int)
options.define("authenticate", group="application", type=bool)
options.define("cookie_secret", group="application", type=str)
options.define("address", group="server", type=str)
options.define("port", group="server", type=int)
routes = []
