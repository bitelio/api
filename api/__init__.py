__author__ = "Guillermo Guirao Aguilar"
__email__ = "info@bitelio.com"
__version__ = "0.0.1"


from tornado import options
from tornado.web import Application

from api import handlers


def start(env: str) -> Application:
    options.parse_config_file(f"api/config/{env}.py")
    settings = options.options.group_dict("application")
    settings["default_handler_class"] = handlers.NotFoundHandler
    return Application(handlers.routes, **settings)


options.define("sg", group="application", type=object)
options.define("log", group="application", type=object)
options.define("mongo", group="application", type=object)
options.define("redis", group="application", type=object)
options.define("debug", group="application", type=bool)
options.define("session", group="application", type=int)
options.define("authenticate", group="application", type=bool)
options.define("compress_response", group="application", type=bool)
options.define("address", group="server", type=str)
options.define("port", group="server", type=int)
