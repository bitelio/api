from http import HTTPStatus
from typing import List, Tuple

from .base import BaseHandler
from .auth import LoginHandler, LogoutHandler


class NotFoundHandler(BaseHandler):
    def prepare(self) -> None:
        self.write_error(404, "Invalid URL")


class StatusHandler(BaseHandler):
    def get(self) -> None:
        return


def handler_log(handler):
    status_code = handler.get_status()
    if not handler.log._context.get("event"):
        status = HTTPStatus(status_code)
        handler.log = handler.log.bind(event=status.phrase)
    if isinstance(handler, StatusHandler):
        log = handler.log.debug
    elif status_code < 400:
        log = handler.log.info
    elif status_code < 500:
        log = handler.log.warning
    else:
        log = handler.log.error
    time = round(1000 * handler.request.request_time(), 2)
    log(status=status_code, time=time)


def configure(mapper, prefix="") -> List[Tuple[str, BaseHandler]]:
    urls: List[Tuple[str, BaseHandler]] = []
    for key, value in mapper.items():
        if isinstance(value, dict):
            urls.extend(configure(value, f"{prefix}/{key}"))
        elif key:
            urls.append((f"{prefix}/{key}", value))
        else:
            urls.append((prefix, value))
    return urls


routes = configure({
    "status": StatusHandler,
    "api": {
        "login": LoginHandler,
        "logout": LogoutHandler
    }
})
