from typing import Any
from rapidjson import loads
from datetime import datetime
from functools import wraps
from tornado.web import HTTPError
from structlog import get_logger

from .base import BaseHandler
from ..services import Services
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
def limiter(handler) -> None:
    username = loads(handler.request.body).get('username')
    key = f"limiter:{username}:{datetime.now().minute}"
    requests = int(Services.redis.get(key) or 0)
    if requests < 3:
        Services.redis.set(key, requests + 1, ex=59)
    else:
        raise HTTPError(429)


@middleware
def debug(handler) -> None:
    if not handler.application.settings.get('debug'):
        raise HTTPError(404)


log = get_logger(__name__)
