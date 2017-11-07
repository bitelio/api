from schematics.types import IntType

from api.models import BaseModel


class BoardModel(BaseModel):
    BoardId = IntType(required=True)

    @property
    def query(self):
        return [{"$match": {"Id": self.BoardId}},
                {"$lookup":
                    {"from": "card_types", "localField": "Id",
                     "foreignField": "BoardId", "as": "CardTypes"}},
                {"$lookup":
                    {"from": "classes_of_service", "localField": "Id",
                     "foreignField": "BoardId", "as": "ClassesOfService"}},
                {"$project":
                    {"_id": 0, "CardTypes._id": 0, "ClassesOfService._id": 0,
                     "CardTypes.BoardId": 0, "ClassesOfService.BoardId": 0}}]
