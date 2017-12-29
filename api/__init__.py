__author__ = "Guillermo Guirao Aguilar"
__email__ = "info@bitelio.com"
__version__ = "0.0.1"


from tornado import options
from tornado.web import Application

from . import utils


def route(handler):
    url = f"/{handler.__name__.lower()[:-7]}"
    parent = handler.__bases__[0]
    while parent.__name__ is not "BaseHandler":
        url = f"/{parent.__name__.lower()[:-7]}" + url
        parent = parent.__bases__[0]
    routes.append((f"/api{url}", handler))
    return handler


def start(env):
    options.parse_config_file(f"api/config/{env}.py")
    return Application(routes, default_handler_class=handlers.NotFoundHandler,
                       **options.options.group_dict("application"))


routes = []
models = utils.load("models")
handlers = utils.load("handlers")
options.define("db", group="application", type=object)
options.define("log", group="application", type=object)
options.define("cache", group="application", type=object)
options.define("debug", group="application", type=bool)
options.define("address", group="server", type=str)
options.define("port", group="server", type=int)
