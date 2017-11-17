from api import route
from api.handlers.board import BoardHandler


@route
class SettingsHandler(BoardHandler):
    async def load(self):
        return await self.db.settings.find_one(self.model.query,
                                               self.model.projection)
