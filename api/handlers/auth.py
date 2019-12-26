from pydantic import BaseModel
from tornado.web import HTTPError

from passlib.hash import argon2
from tortoise.exceptions import DoesNotExist

from ..models.user import User
from ..models.session import Session, Token
from .base import BaseHandler, endpoint
from .middleware import authenticator, limiter


class Credentials(BaseModel):
    username: str
    password: str


class LoginHandler(BaseHandler):
    @endpoint(limiter)
    async def post(self, body: Credentials) -> Token:
        user = await User.get_or_none(username=body.username)
        if user:
            self.log = self.log.bind(user=user.username)
            if argon2.verify(body.password, user.password):
                self.log = self.log.bind(event=f"Logged in {user.username}")
                session = Session.new(user.username, user.role)
                return session.token
        raise HTTPError(401, reason=f"Invalid credentials")


class LogoutHandler(BaseHandler):
    @endpoint(authenticator)
    async def get(self) -> None:
        self.session.end()
        self.log = self.log.bind(event=f"Logged out {self.session.username}")
