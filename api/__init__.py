__author__ = "Guillermo Guirao Aguilar"
__email__ = "info@bitelio.com"
__version__ = "0.0.1"


from asyncio import get_event_loop
from logging import getLogger
from logging.config import dictConfig
from tornado.web import Application
from tornado.platform.asyncio import AsyncIOMainLoop
from motor.motor_tornado import MotorClient
from pymongo import MongoClient
from redis import StrictRedis

from . import config, utils


def route(handler):
    url = f"/{handler.__name__.lower()[:-7]}"
    parent = handler.__bases__[0]
    while parent.__name__ is not "BaseHandler":
        url = f"/{parent.__name__.lower()[:-7]}" + url
        parent = parent.__bases__[0]
    routes.append((url, handler))
    return handler


def start(**kwargs):
    global db, cache, boards
    log.info("Starting api")
    for key, value in kwargs.items():
        setattr(config, key, value)
    db = MotorClient(config.mongo, tz_aware=True).get_default_database()
    cache = StrictRedis(config.redis)
    pymongo = MongoClient(config.mongo).get_default_database()
    boards = [board["Id"] for board in pymongo.boards.find()]
    return Application(routes, default_handler_class=handlers.NotFoundHandler,
                       debug=config.debug)


def run(app=None):
    AsyncIOMainLoop().install()
    (app or start()).listen(port=config.port)
    log.info(f"Listening on {config.port}")
    get_event_loop().run_forever()


routes = []
log = getLogger(__name__)
dictConfig(config.logging)
handlers = utils.load("handlers")
models = utils.load("models")
