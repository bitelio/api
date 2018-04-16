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

    def validate_password(self, value):
        if len(value) < 6:
            msg = "Your password must be at least 6 characters long"
            raise ValidationError(msg)
        return value

    def hash(self):
        return argon2.hash(self.Password)

    def verify(self, password):
        return argon2.verify(self.Password, password)


class TokenModel(Model):
    Token = StringType(required=True)


class Subscriptions(Model):
    Alerts = BooleanType(default=False)
    Updates = BooleanType(default=False)


class UserModel(PasswordModel):
    Locale = StringType(choices=["en", "de"], default="en")
    Subscriptions = ModelType(Subscriptions)

    def to_native(self, *args, **kwargs):
        data = super().to_native(*args, **kwargs)
        if "Password" in data:
            data["Password"] = self.hash()
        return data
