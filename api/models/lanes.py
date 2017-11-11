from schematics.types import StringType

from api.models.board import BoardModel


class LanesModel(BoardModel):
    Stage = StringType(choices=["backlog", "wip", "archive"])

    fields = ["Id", "Title", "Index", "Width", "Orientation", "ChildLaneIds"]

    @property
    def query(self):
        return self.to_native()
