from typing import Any
from functools import wraps
from tornado.web import HTTPError, RequestHandler

from ..models.session import Session, DoesNotExist


def middleware(function):
    @wraps(function)
    def decorator(method):
        @wraps(method)
        async def wrapper(handler: RequestHandler, *args, **kwargs) -> Any:
            try:
                function(handler)
            except HTTPError as error:
                handler.send_error(error.status_code, reason=error.reason)
            else:
                return await method(handler, *args, **kwargs)
        return wrapper
    return decorator


@middleware
def authenticator(handler: RequestHandler) -> None:
    try:
        handler.session = Session.get(handler.get_cookie("token", ""))
    except DoesNotExist:
        raise HTTPError(401)


@middleware
def limiter(handler):
    return
    if handler.services.limiter.check():
        raise HTTPError(429)
    else:
        handler.services.limiter.set(handler.request.remote_ip)
