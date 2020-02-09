from http import HTTPStatus

from .base import BaseHandler, endpoint
from .middleware import debug


class FastlaneHandler(BaseHandler):
    @endpoint(debug)
    def get(self) -> HTTPStatus:
        return HTTPStatus.OK
