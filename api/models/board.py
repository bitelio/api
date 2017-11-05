from schematics.types import IntType

from api.models import BaseModel


class BoardModel(BaseModel):
    BoardId = IntType(required=True)

    @property
    def query(self):
        pipeline = [{"$match": {"Id": self.BoardId}},
                    {"$lookup":
                        {"from": "card_types", "localField": "Id",
                         "foreignField": "BoardId", "as": "CardTypes"}},
                    {"$lookup":
                        {"from": "classes_of_service", "localField": "Id",
                         "foreignField": "BoardId", "as": "ClassesOfService"}}]
        return pipeline
