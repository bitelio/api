from motor.motor_tornado import MotorClient
from fakeredis import FakeStrictRedis


mongo = MotorClient(tz_aware=True)["test"]
redis = FakeStrictRedis()
# sg = mock()
port = 8008
logging = None
