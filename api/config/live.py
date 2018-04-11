from os import getenv
from motor.motor_tornado import MotorClient
from redis import StrictRedis
from sendgrid import SendGridAPIClient
from logging import getLogger


mongo = MotorClient("mongo", tz_aware=True)["kanban"]
redis = StrictRedis("redis")
sg = SendGridAPIClient(apikey=getenv('SENDGRID'))
log = getLogger("tornado.api")
port = 80
compress_response = True
authenticate = True
session = 60 * 60 * 24 * 30
