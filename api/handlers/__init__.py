from http import HTTPStatus
from typing import List, Tuple
from tornado.web import RequestHandler
from prometheus_client import REGISTRY
from prometheus_client.exposition import choose_encoder

from .base import BaseHandler
from .auth import LoginHandler, LogoutHandler
from .user import ProfileHandler
from .debug import FastlaneHandler


class NotFoundHandler(BaseHandler):
    def prepare(self) -> None:
        self.write_error(404, "Invalid URL")


class StatusHandler(BaseHandler):
    def get(self) -> None:
        return


class MetricsHandler(BaseHandler):
    registry = REGISTRY

    def get(self) -> None:
        registry = self.registry
        accept = self.request.headers.get("Accept")
        encoder, content_type = choose_encoder(accept)
        name = self.get_argument("name", None)
        if name:
            registry = registry.restricted_registry(name)
        output = encoder(registry)
        self.set_header("Content-Type", content_type)
        self.write(output)


def handler_log(handler):
    status_code = handler.get_status()
    if not handler.log._context.get("event"):
        status = HTTPStatus(status_code)
        handler.log = handler.log.bind(event=status.phrase)
    if isinstance(handler, (StatusHandler, MetricsHandler)):
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


routes = configure(
    {
        "status": StatusHandler,
        "metrics": MetricsHandler,
        "api": {
            "login": LoginHandler,
            "logout": LogoutHandler,
            "profile": ProfileHandler,
            "fastlane": FastlaneHandler,
        },
    }
)
