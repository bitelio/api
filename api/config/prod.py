from sys import getenv
from motor.motor_tornado import MotorClient
from redis import StrictRedis
from logging import getLogger


db = MotorClient("mongo", tz_aware=True)["kanban"]
cache = StrictRedis("redis")
log = getLogger("tornado.api")
port = 80
compress_response = True
cookie_secret = getenv("API_SECRET")
