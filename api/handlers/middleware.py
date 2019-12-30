from typing import Any
from functools import wraps
from tornado.web import HTTPError
from structlog import get_logger

from .base import BaseHandler
from ..models.session import Session, DoesNotExist


def middleware(function):
    @wraps(function)
    def decorator(method):
        @wraps(method)
        async def wrapper(handler: BaseHandler, *args, **kwargs) -> Any:
            try:
                function(handler)
            except HTTPError as error:
                handler.send_error(error.status_code, reason=error.reason)
            else:
                return await method(handler, *args, **kwargs)

        return wrapper

    return decorator


@middleware
def authenticator(handler: BaseHandler) -> None:
    token = handler.get_cookie("token")
    if token:
        try:
            handler.session = Session.get(token)
            return
        except DoesNotExist:
            log.debug("Invalid token")
    else:
        log.debug("Missing token")
    raise HTTPError(401)


@middleware
def limiter(handler):
    return
    if handler.services.limiter.check():
        raise HTTPError(429)
    else:
        handler.services.limiter.set(handler.request.remote_ip)


log = get_logger(__name__)
