from motor.motor_tornado import MotorClient
from fakeredis import FakeStrictRedis
from logging import getLogger


db = MotorClient(tz_aware=True)["kanban"]
cache = FakeStrictRedis()
log = getLogger("tornado.api")
logging = "debug"
address = "127.0.0.1"
port = 5000
debug = True
