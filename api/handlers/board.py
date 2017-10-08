from schematics.types import IntType

from api import route, cache
from api.handlers import BaseHandler, BaseModel


@route
class BoardHandler(BaseHandler):
    async def post(self):
        self.check(await self.db.boards.aggregate(self.model.query))

    async def check(self, data):
        if data:
            self.write(data)
        elif await self.exists():
            self.write([])
        else:
            self.write_error(404, f"Board {self.model.BoardId} not found")

    async def exists(self):
        return await self.db.boards.find_one({"Id": self.model.BoardId})


class BoardModel(BaseModel):
    BoardId = IntType(required=True)

    @property
    def query(self):
        ignored = cache.board[self.BoardId]["Ignored"]
        pipeline = [{"$match": {"Id": self.BoardId}},
                    {"$lookup":
                        {"from": "card_types", "localField": "Id",
                         "foreignField": "BoardId", "as": "CardTypes"}},
                    {"$lookup":
                        {"from": "classes_of_service", "localField": "Id",
                         "foreignField": "BoardId", "as": "ClassesOfService"}}]
        if ignored["TypeId"]:
            match = {"CardTypes.Id": {"$ne": ignored["TypeId"]}}
            pipeline.append(({"$match": match}))
        if ignored["ClassOfServiceId"]:
            match = {"ClassesOfService.Id": {"$ne": ignored["ClassOfServiceId"]}}
            pipeline.append(({"$match": match}))
        return pipeline
