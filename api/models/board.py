from schematics.models import Model
from schematics.types import IntType, FloatType, StringType
from schematics.types.compound import ListType, ModelType
from schematics.exceptions import DataError

from .base import ListModel


class StationModel(Model):
    Card = FloatType(default=0, min_value=0)
    Lanes = ListType(IntType, default=[])
    Name = StringType(required=True)
    Phase = StringType()
    Size = FloatType(default=0, min_value=0)


class StationsModel(ListModel):
    Body = ListType(ModelType(StationModel), required=True)

    def validate(self, partial=False, convert=True, app_data=None, **kwargs):
        super().validate(partial, convert, app_data, **kwargs)
        ids = [lane for station in self.Body for lane in station.Lanes]
        duplicates = set([lane for lane in ids if ids.count(lane) > 1])
        if duplicates:
            raise DataError({"Duplicate lanes": duplicates})
