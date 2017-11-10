from schematics.models import Model
from schematics.types import IntType, FloatType, StringType
from schematics.types.compound import ListType, ModelType
from schematics.exceptions import DataError

from api.models.board import BoardModel


class StationModel(Model):
    Card = FloatType(default=0, min_value=0)
    Lanes = ListType(IntType, default=[])
    Name = StringType(required=True)
    Phase = StringType()
    Size = FloatType(default=0, min_value=0)


class StationsModel(BoardModel):
    class PUT(Model):
        Stations = ListType(ModelType(StationModel), required=True)

        def validate(self, partial=False, convert=True, app_data=None, **args):
            super().validate(partial, convert, app_data, **args)
            ids = [lane for station in self.Stations for lane in station.Lanes]
            duplicates = set([lane for lane in ids if ids.count(lane) > 1])
            if duplicates:
                raise DataError({"Duplicate lanes": duplicates})

    @property
    def match(self):
        return {"$match": {"BoardId": self.BoardId}}

    @property
    def query(self):
        return {"BoardId": self.BoardId}

    @property
    def projection(self):
        fields = {key: 1 for key in StationModel().keys()}
        fields.update({"_id": 0})
        return fields

    @property
    def payload(self):
        stations = self.to_native()["Stations"]
        for position, station in enumerate(stations):
            station["Position"] = position
            station["BoardId"] = self.BoardId
        return stations
