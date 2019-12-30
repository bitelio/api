from .base import BaseHandler, endpoint
from .middleware import debug


class FastlaneHandler(BaseHandler):
    @endpoint(debug)
    async def get(self) -> None:
        return
