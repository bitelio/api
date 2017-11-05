from schematics.types import StringType

from api.models.board import BoardModel


class LanesModel(BoardModel):
    Stage = StringType(choices=["backlog", "wip", "archive"])

    @property
    def query(self):
        return self.to_native()

    @property
    def projection(self):
        return {"_id": 0}
