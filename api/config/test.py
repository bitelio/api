from motor.motor_tornado import MotorClient
from fakeredis import FakeStrictRedis
from logging import getLogger


db = MotorClient(tz_aware=True)["test"]
cache = FakeStrictRedis()
log = getLogger("tornado.api")
port = 8008
cookie_secret = "xxx"
