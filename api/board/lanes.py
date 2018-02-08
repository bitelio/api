from api import route
from api.board import BoardHandler, BaseBoardModel


class LanesModel(BaseBoardModel):
    fields = ["Id", "Title", "Top", "Width", "Height", "Left", "ChildLaneIds"]


@route
class LanesHandler(BoardHandler):
    async def load(self):
        cursor = self.db.lanes.find(self.model.query, self.model.projection)
        return await cursor.to_list(None)
