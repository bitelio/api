from schematics.types import StringType

from api.board import BoardHandler, BoardModel


class LanesModel(BoardModel):
    fields = ["Id", "Title", "Top", "Width", "Height", "Left", "ChildLaneIds"]

    @property
    def query(self):
        return self.to_native()


class LanesHandler(BoardHandler):
    async def load(self):
        cursor = self.db.lanes.find(self.model.query, self.model.projection)
        return await cursor.to_list(None)
