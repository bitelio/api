from schematics.types import IntType

from api.models import BaseModel


class BoardModel(BaseModel):
    BoardId = IntType(required=True)

    fields = ["Id", "Title", "AvailableTags",
              {"CardTypes": ["Id", "Name", "Ignore"],
               "ClassesOfService": ["Id", "Title", "Ignore"]}]

    @property
    def projection(self):
        fields = {"_id": 0}
        for field in self.fields:
            if isinstance(field, str):
                fields[field] = 1
            elif isinstance(field, dict):
                for name, subitems in field.items():
                    for item in subitems:
                        fields[f"{name}.{item}"] = 1
            else:
                raise ValueError("Invalid fields format")
        return fields

    @property
    def query(self):
        return [{"$match": {"Id": self.BoardId}},
                {"$lookup":
                    {"from": "card_types", "localField": "Id",
                     "foreignField": "BoardId", "as": "CardTypes"}},
                {"$lookup":
                    {"from": "classes_of_service", "localField": "Id",
                     "foreignField": "BoardId", "as": "ClassesOfService"}},
                {"$project": self.projection}]
