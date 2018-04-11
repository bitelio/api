from schematics.models import Model
from schematics.types import StringType


class AuthModel(Model):
    UserName = StringType(required=True)
    Password = StringType(required=True)
