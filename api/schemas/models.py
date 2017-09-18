from schematics.models import Model
from schematics.types import ListType
from schematics.types import IntType
from schematics.types import StringType

from .types import KanbanIdType


class Query(Model):
    def serialize(self):
        query = {}
        for key, value in self.items():
            if value:
                if isinstance(value, list):
                    if len(value) == 1:
                        query[key] = value[0]
                    else:
                        query[key] = {'$in': value}
                else:
                    query[key] = value
        return query


class Cards(Query):
    Priority = ListType(IntType(min_value=0, max_value=4))
    TypeId = ListType(KanbanIdType)
    ClassOfService = ListType(KanbanIdType)


class Station(Model):
    Position = IntType(required=True)
    Title = StringType(required=True)
    Lanes = ListType(KanbanIdType, required=True)
    BoardId = KanbanIdType(required=True)


class Phase(Model):
    Title = StringType(required=True)
    Stations = ListType(StringType, required=True)
    BoardId = KanbanIdType(required=True)
