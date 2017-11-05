from schematics.types.net import EmailType

from api.models import BaseModel


class UserModel(BaseModel):
    UserName = EmailType(required=True)

    @property
    def query(self):
        return [{"$match": {"UserName": self.UserName.lower()}},
                {"$lookup": {"from": "boards", "localField": "BoardId",
                             "foreignField": "Id", "as": "Board"}}]
