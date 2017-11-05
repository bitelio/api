from copy import deepcopy

import api
from api.handlers.board import BoardHandler


@api.route
class StationsHandler(BoardHandler):
    async def load(self):
        cursor = api.db.stations.find(self.model.query, self.model.projection)
        return await cursor.to_list(100)

    async def put(self):
        payload = self.model.payload
        await api.db.stations.remove(self.model.query)
        if payload:
            await api.db.stations.insert_many(deepcopy(payload))
        self.write(payload)
