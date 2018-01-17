from schematics.types import StringType

from api import route
from api.board import BoardHandler, BoardModel


class LanesModel(BoardModel):
    Stage = StringType(choices=["backlog", "wip", "archive"], default="wip")

    fields = ["Id", "Title", "Index", "Width", "Orientation",
              "ChildLaneIds", "ParentLaneId"]

    @property
    def query(self):
        return self.to_native()


@route
class LanesHandler(BoardHandler):
    async def load(self):
        cursor = self.db.lanes.find(self.model.query, self.model.projection)
        return self.arrange(await cursor.to_list(None))

    @staticmethod
    def arrange(lanes):
        table = {lane["Id"]: lane for lane in lanes}
        for lane in lanes:
            lane["ChildLanes"] = [table[id] for id in lane["ChildLaneIds"]]
            del lane["ChildLaneIds"]
        return [lane for lane in lanes if not lane["ParentLaneId"]]
