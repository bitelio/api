from motor.motor_tornado import MotorClient
from fakeredis import FakeStrictRedis
from structlog.dev import ConsoleRenderer
from structlog.processors import TimeStamper

from api import config


processors = [TimeStamper(fmt="%Y-%m-%d %H:%M:%S"), ConsoleRenderer()]
config.processors.extend(processors)
config.log.setLevel("DEBUG")
config.configure(processors=config.processors)
mongo = MotorClient(tz_aware=True)["test"]
redis = FakeStrictRedis()
cookie = '{"UserName": "user1@example.org", "Boards": {"100000000": 4}}'
redis.set("session:xxx", cookie)
address = "127.0.0.1"
port = 5000
debug = True
logging = None
