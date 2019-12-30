from enum import IntEnum
from tortoise.models import Model
from tortoise.fields import CharField, IntEnumField

Role = IntEnum("Role", ("guest", "user", "admin"))


class User(Model):
    username: str = CharField(pk=True, max_length=32)
    password: str = CharField(max_length=80)
    email: str = CharField(unique=True, max_length=64)
    role: Role = IntEnumField(Role)
