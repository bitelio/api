from motor.motor_tornado import MotorClient
from fakeredis import FakeStrictRedis

from api.config import log
from api.config.util import Mock


mongo = MotorClient(tz_aware=True)["test"]
redis = FakeStrictRedis()
sg = Mock(log)
port = 8008
logging = None
