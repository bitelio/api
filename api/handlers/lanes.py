from schematics.types import StringType

from api import route
from api.handlers.board import BoardHandler, BoardModel


@route
class LanesHandler(BoardHandler):
    async def post(self):
        cursor = self.db.lanes.find(self.model.query, self.model.projection)
        await self.check(await cursor.to_list(100))


class LanesModel(BoardModel):
    Stage = StringType(choices=["backlog", "wip", "archive"])

    @property
    def query(self):
        return self.to_native()

    @property
    def projection(self):
        return {"_id": 0}
