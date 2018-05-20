from passlib.hash import argon2
from schematics.models import Model
from schematics.types import BooleanType, StringType, ModelType
from schematics.exceptions import ValidationError


class UsernameModel(Model):
    UserName = StringType(required=True)

    def __init__(self, raw_data, *args, **kwargs):
        if "UserName" in raw_data and isinstance(raw_data["UserName"], str):
            raw_data["UserName"] = raw_data["UserName"].strip().lower()
        super().__init__(raw_data, *args, **kwargs)


class PasswordModel(Model):
    Password = StringType(required=True)

    @staticmethod
    def validate_password(value):
        if isinstance(value, str) and len(value) < 6:
            msg = "Your password must be at least 6 characters long"
            raise ValidationError(msg)
        return value

    def hash(self) -> str:
        return argon2.hash(self.Password)

    def verify(self, password: str) -> bool:
        return argon2.verify(self.Password, password)


class TokenModel(Model):
    Token = StringType(required=True)


class Subscriptions(Model):
    Alerts = BooleanType()
    Updates = BooleanType()


class UserModel(PasswordModel, UsernameModel):
    Locale = StringType(choices=["en", "de"], default="en")
    Password = StringType()
    Signed = BooleanType(choices=[True])
    Subscriptions = ModelType(Subscriptions)
    UserName = StringType()
    Token = StringType()

    def to_native(self, *args, **kwargs) -> dict:
        data = super().to_native(*args, **kwargs)
        if "Password" in data:
            data["Password"] = self.hash()
        return data

    class Options:
        serialize_when_none = False
