from .base import BaseHandler
from .user import UserHandler
from .login import LoginHandler
from .logout import LogoutHandler
from .password import PasswordHandler
from . import board


class NotFoundHandler(BaseHandler):
    def prepare(self):
        self.write_error(404, "Invalid URL")


def logger(handler):
    status_code = handler.get_status()
    if status_code < 400:
        log = handler.log.info
    elif status_code < 500:
        log = handler.log.warning
    else:
        log = handler.log.error
    time = round(1000 * handler.request.request_time(), 2)
    log(getattr(handler, "message", ""), status=status_code, time=time)


def configure(mapper, prefix=""):
    urls = []
    for key, value in mapper.items():
        if isinstance(value, dict):
            urls.extend(configure(value, f"{prefix}/{key}"))
        elif key:
            urls.append((f"{prefix}/{key}", value))
        else:
            urls.append((prefix, value))
    return urls


routes = configure({
    "api": {
        "user": UserHandler,
        "login": LoginHandler,
        "logout": LogoutHandler,
        "password": PasswordHandler,
        "(?P<board_id>\d+)": board.routes
    }
})
