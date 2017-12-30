from copy import deepcopy
from schematics.models import Model
from schematics.types import IntType, FloatType, StringType
from schematics.types.compound import ListType, ModelType
from schematics.exceptions import DataError

from api import route
from api.board import BoardHandler, BoardModel


class StationModel(Model):
    Card = FloatType(default=0, min_value=0)
    Lanes = ListType(IntType, default=[])
    Name = StringType(required=True)
    Phase = StringType()
    Size = FloatType(default=0, min_value=0)


class StationsModel(BoardModel):
    fields = ["Name", "Card", "Size", "Lanes", "Phase"]

    class PUT(Model):
        Stations = ListType(ModelType(StationModel), required=True)

        def validate(self, partial=False, convert=True, app_data=None, **args):
            super().validate(partial, convert, app_data, **args)
            ids = [lane for station in self.Stations for lane in station.Lanes]
            duplicates = set([lane for lane in ids if ids.count(lane) > 1])
            if duplicates:
                raise DataError({"Duplicate lanes": duplicates})

    @property
    def query(self):
        return {"BoardId": self.BoardId}

    @property
    def payload(self):
        stations = self.to_native()["Stations"]
        for position, station in enumerate(stations):
            station["Position"] = position
            station["BoardId"] = self.BoardId
        return stations


@route
class StationsHandler(BoardHandler):
    async def load(self):
        cursor = self.db.stations.find(self.model.query, self.model.projection)
        return await cursor.to_list(100)

    async def put(self):
        payload = self.model.payload
        await self.db.stations.remove(self.model.query)
        if payload:
            await self.db.stations.insert_many(deepcopy(payload))
        self.write(payload)
