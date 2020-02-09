from datetime import datetime
from functools import wraps
from typing import Any, Callable

from structlog import get_logger
from tornado.web import HTTPError

from rapidjson import loads

from ..models.session import DoesNotExist, Session
from ..services import Services
from .base import BaseHandler


def middleware(function: Callable[[BaseHandler], None]
               ) -> Callable[[Callable[..., Any]], Callable[..., None]]:
    @wraps(function)
    def decorator(method: Callable[..., Any]) -> Callable[..., None]:
        @wraps(method)
        async def wrapper(handler: BaseHandler, *args, **kwargs) -> None:
            try:
                function(handler)
            except HTTPError as error:
                handler.send_error(error.status_code, reason=error.reason)
            else:
                await method(handler, *args, **kwargs)

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
def limiter(handler: BaseHandler) -> None:
    username = loads(handler.request.body or "{}").get('username')
    key = f"limiter:{username}:{datetime.now().minute}"
    requests = int(Services.redis.get(key) or 0)
    if requests < 3:
        Services.redis.set(key, requests + 1, ex=59)
    else:
        raise HTTPError(429)


@middleware
def debug(handler: BaseHandler) -> None:
    if not handler.application.settings.get('debug'):
        raise HTTPError(404)


log = get_logger(__name__)
