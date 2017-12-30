from schematics.types import StringType

from api import route
from api.board import BoardHandler, BoardModel


class LanesModel(BoardModel):
    Stage = StringType(choices=["backlog", "wip", "archive"])

    fields = ["Id", "Title", "Index", "Width", "Orientation", "ChildLaneIds"]

    @property
    def query(self):
        return self.to_native()


@route
class LanesHandler(BoardHandler):
    async def load(self):
        cursor = self.db.lanes.find(self.model.query, self.model.projection)
        return await cursor.to_list(100)
