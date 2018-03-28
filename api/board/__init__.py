from json import loads
from datetime import datetime
from schematics.types import IntType

from api.base import BaseHandler, BaseModel


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
        cached = self.cache.get(self.model.id)
        if cached:
            self.write(cached)
            self.request.cached = True
        else:
            self.write(await self.load())
            pipeline = self.cache.pipeline()
            pipeline.set(self.model.id, b"".join(self._write_buffer))
            pipeline.set(self.model["BoardId"], self.model.id)
            pipeline.execute()

    def on_finish(self):
        if self.request.method == 'PUT':
            event = {"data": self.model.payload,
                     "date": datetime.today(),
                     "path": self.request.path}
            self.db.history.insert_one(event)

    async def exists(self):
        cached = self.cache.get("boards")
        if cached:
            boards = loads(cached.decode())
        else:
            boards = await self.db.boards.find().distinct("Id")
            self.cache.set("boards", boards)
        return self.model.BoardId in boards

    def _request_summary(self):
        cached = " cached" if getattr(self.request, "cached", False) else " -"
        return super()._request_summary() + cached
