from datetime import datetime
from secrets import token_hex

from rapidjson import loads
from squema import Squema
from structlog import get_logger

from .. import Services
from .user import Role


class DoesNotExist(Exception):
    pass


class Token(str):
    @classmethod
    def new(cls, length: int = 16) -> "Token":
        return Token(token_hex(length))


class Session(Squema):
    username: str
    token: Token
    role: Role
    date: datetime

    @classmethod
    def new(cls, username: str, role: str) -> 'Session':
        log.debug(f"New session for {username}")
        session = cls(
            username=username,
            token=Token.new(),
            role=role,
            date=datetime.today())
        duration = 60 * 60 * 24 * 12
        Services.redis.set(session.token, str(session), duration)
        return session

    @classmethod
    def get(cls, token: str) -> 'Session':
        session = Services.redis.get(token)
        if session:
            return cls(**loads(session))
        raise DoesNotExist

    def end(self) -> None:
        log.debug(f"Closing session for user {self.username}")
        Services.redis.delete(self.token)


log = get_logger(__name__)
