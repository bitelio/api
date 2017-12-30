from api import route
from api.board import BoardHandler, BoardModel


class SettingsModel(BoardModel):
    fields = ["OfficeHours", "Holidays", "Timezone", "Ignore"]

    @property
    def query(self):
        return {"Id": self.BoardId}


@route
class SettingsHandler(BoardHandler):
    async def load(self):
        return await self.db.settings.find_one(self.model.query,
                                               self.model.projection)
