from motor.motor_tornado import MotorClient
from fakeredis import FakeStrictRedis
from logging import getLogger


mongo = MotorClient(tz_aware=True)["test"]
redis = FakeStrictRedis()
log = getLogger("tornado.api")
port = 8008
