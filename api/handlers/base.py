from functools import wraps
from inspect import isawaitable
from http import HTTPStatus
from inspect import signature
from types import TracebackType
from typing import Any, Callable, Optional, Type

from prometheus_client import Histogram
from pydantic import ValidationError
from squema import Squema
from structlog import get_logger
from tornado.web import HTTPError, RequestHandler

from rapidjson import JSONDecodeError, loads

from api.models import Session


class BaseHandler(RequestHandler):
    SUPPORTED_METHODS = ("GET", "POST", "DELETE", "", "", "", "")
    session: Session
    metrics = Histogram(
        "api_request_duration_seconds",
        "Request latency",
        ("handler", "method", "status"),
    )

    def initialize(self):
        log_info = ["method", "path", "remote_ip", "query"]
        self.log = get_logger("api.handlers").bind(
            **{key: getattr(self.request, key) for key in log_info}
        )

    def log_exception(
        self,
        exception_type: Optional[Type[BaseException]],
        value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        if isinstance(value, HTTPError):
            if value.log_message:
                self.log.warning(value.log_message, status=value.status_code)
        else:
            self.log.error(
                "Uncaught exception",
                exc_info=(exception_type, value, traceback),
            )

    def write(self, data: Any) -> None:
        if isinstance(data, (str, int, float)):
            super().write({data.__class__.__name__.lower(): data})
        elif isinstance(data, Squema):
            super().write(str(data))
        else:
            super().write(data)

    def write_error(self, status_code=None, message=None, **kwargs):
        self.set_status(status_code or self._status_code)
        self.log = self.log.bind(event=message)
        self.write({"code": status_code, "message": message})
        self.finish()

    def on_finish(self) -> None:
        self.metrics.labels(
            handler=self.name,
            method=self.request.method,
            status=self.get_status(),
        ).observe(self.request.request_time())

    @property
    def name(self) -> str:
        return self.__class__.__name__


def endpoint(*middleware) -> Callable[..., Any]:
    def decorator(method):
        @wraps(method)
        async def wrapper(self, *args, **kwargs) -> None:
            if schema:  # type: ignore
                try:
                    data = loads(self.request.body or "{}")
                    body = schema(**data)  # type: ignore
                except JSONDecodeError:
                    return self.send_error(400, message="Invalid body format")
                except ValidationError as exception:
                    error = exception.errors()[0]
                    return self.send_error(
                        400, message=f"{error['loc'][0]}: {error['msg']}"
                    )
                kwargs["body"] = body
            response = method(self, *args, **kwargs)
            if isawaitable(response):
                response = await response
            if response:
                if response is HTTPStatus:
                    self.set_status(response, reason=response.phrase)
                    self.finish()
                else:
                    self.finish(response)

        body = signature(method).parameters.get("body")
        schema = getattr(body, "annotation", None)
        for function in reversed(middleware):
            wrapper = function(wrapper)
        return wrapper

    return decorator
