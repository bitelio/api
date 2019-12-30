from squema import Squema

from .base import BaseHandler, endpoint
from .middleware import authenticator
from ..models import User, Role


class Profile(Squema):
    username: str
    email: str
    role: Role


class ProfileHandler(BaseHandler):
    @endpoint(authenticator)
    async def get(self) -> Profile:
        user = await User.get(username=self.session.username).values()
        return Profile(**user[0])
