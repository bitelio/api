from motor.motor_tornado import MotorClient
from fakeredis import FakeStrictRedis
from logging import getLogger


mongo = MotorClient(tz_aware=True)["kanban"]
redis = FakeStrictRedis()
log = getLogger("tornado.api")
logging = "debug"
address = "127.0.0.1"
port = 5000
debug = True
