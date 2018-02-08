from datetime import datetime
from schematics.types import IntType

from api import route
from api.base import BaseHandler, BaseModel


class BaseBoardModel(BaseModel):
    BoardId = IntType(required=True)

    @property
    def query(self) -> dict:
        return self.to_native()

    @property
    def projection(self) -> dict:
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
    def key(self):
        return f'{self.BoardId}:{self.name}:{self.id}'


class BoardModel(BaseBoardModel):
    fields = ["Id", "Title", "AvailableTags",
              {"CardTypes": ["Id", "Name", "Ignore"],
               "ClassesOfService": ["Id", "Title", "Ignore"]}]

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


@route
class BoardHandler(BaseHandler):
    async def prepare(self):
        super().prepare()
        if not self._finished and not await self.exists():
            self.write_error(404, f"Board {self.model.BoardId} not found")

    async def load(self):
        cursor = self.db.boards.aggregate(self.model.query)
        await cursor.fetch_next
        return cursor.next_object()

    async def post(self):
        if self.cache.exists(self.model.id):
            self.write(self.cache.get(self.model.id))
            self.request.cached = True
        else:
            self.write(await self.load())
            self.cache.set(self.model.key, b"".join(self._write_buffer))

    def on_finish(self):
        if self.request.method == 'PUT':
            event = {"data": self.model.payload,
                     "date": datetime.today(),
                     "path": self.request.path}
            self.db.history.insert_one(event)

    async def exists(self):
        if not self.cache.exists(self.model.BoardId):
            if not await self.db.boards.find_one({"Id": self.model.BoardId}):
                return False
            self.cache.set(self.model.BoardId, True)
        return True

    def _request_summary(self):
        cached = " cached" if getattr(self.request, "cached", False) else " -"
        return super()._request_summary() + cached
