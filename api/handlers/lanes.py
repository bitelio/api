from api import route
from api.handlers.board import BoardHandler


@route
class LanesHandler(BoardHandler):
    async def load(self):
        cursor = self.db.lanes.find(self.model.query, self.model.projection)
        return await cursor.to_list(100)
