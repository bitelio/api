from os import getenv
from pathlib import Path
from logging import getLogger
from motor.motor_tornado import MotorClient
from redis import StrictRedis
from sendgrid import SendGridAPIClient
from raven.conf import setup_logging
from structlog.processors import JSONRenderer
from logging.handlers import RotatingFileHandler
from raven.handlers.logging import SentryHandler
from pythonjsonlogger.jsonlogger import JsonFormatter

from api import config


class CustomJsonFormatter(JsonFormatter):
    def add_fields(self, log, record, message):
        super().add_fields(log, record, message)
        log["level"] = log.pop("levelname", "").lower()
        log["event"] = log.pop("message", "")


access_log = getLogger("tornado.access")
application_log = getLogger("tornado.application")
general_log = getLogger("tornado.general")

logs = "/var/log/api"
Path(logs).mkdir(parents=True, exist_ok=True)
access_handler = RotatingFileHandler(f"{logs}/access.log", "a", 5**10, 2)
health_handler = RotatingFileHandler(f"{logs}/health.log", "a", 5**10, 2)
formatter = CustomJsonFormatter("(levelname) (name) (message)")
health_handler.setFormatter(formatter)

access_log.addHandler(access_handler)
general_log.addHandler(health_handler)
application_log.addHandler(health_handler)

sentry_handler = SentryHandler(getenv("SENTRY", ""))
sentry_handler.setLevel("ERROR")
setup_logging(sentry_handler)
config.processors.append(JSONRenderer())
config.configure(processors=config.processors)
config.log.setLevel("INFO")

mongo = MotorClient("mongo", tz_aware=True)["bitelio"]
sg = SendGridAPIClient(apikey=getenv("SENDGRID"))
redis = StrictRedis("redis")
ipstack = getenv("APISTACK")

port = 80
compress_response = True
session = 60 * 60 * 24 * 30
logging = None
