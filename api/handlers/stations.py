from copy import deepcopy

from api import route
from api.handlers.board import BoardHandler


@route
class StationsHandler(BoardHandler):
    async def load(self):
        cursor = self.db.stations.find(self.model.query, self.model.projection)
        return await cursor.to_list(100)

    async def put(self):
        payload = self.model.payload
        await self.db.stations.remove(self.model.query)
        if payload:
            await self.db.stations.insert_many(deepcopy(payload))
        self.write(payload)
