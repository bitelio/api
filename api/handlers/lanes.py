import api
from api.handlers.board import BoardHandler


@api.route
class LanesHandler(BoardHandler):
    async def load(self):
        cursor = api.db.lanes.find(self.model.query, self.model.projection)
        return await cursor.to_list(100)
