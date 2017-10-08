__author__ = "Guillermo Guirao Aguilar"
__email__ = "info@bitelio.com"
__version__ = "0.0.1"


from re import match
from os import listdir, path
from asyncio import get_event_loop
from logging import getLogger
from logging.config import dictConfig
from importlib import import_module
from tornado.web import Application
from tornado.platform.asyncio import AsyncIOMainLoop
from motor.motor_tornado import MotorClient

from . import config


def route(handler):
    url = f"/{handler.__name__.lower()[:-7]}"
    parent = handler.__bases__[0]
    while parent.__name__ is not "BaseHandler":
        url = f"/{parent.__name__.lower()[:-7]}" + url
        parent = parent.__bases__[0]
    routes.append((url, handler))
    return handler


def load(name):
    dirname = path.join(path.dirname(__file__), name)
    module = import_module(f"api.{name}")
    for filename in listdir(dirname):
        if match("[a-z]+.py", filename):
            feature = filename[:-3]
            setattr(module, feature, import_module(f"api.{name}.{feature}"))
    return module


def app(**kwargs):
    config.application.update(kwargs)
    dictConfig(config.logging)
    db = MotorClient(**config.database).get_default_database()
    return Application(routes, default_handler_class=handlers.NotFoundHandler,
                       db=db, **config.application)


def run(**kwargs):
    config.server.update(kwargs)
    log.info("Starting api")
    AsyncIOMainLoop().install()
    app().listen(**config.server)
    get_event_loop().run_forever()


log = getLogger(__name__)
routes = []
cache = {}
handlers = load("handlers")
