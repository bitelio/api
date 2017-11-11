from json import loads

from api import route
from api.handlers import BaseHandler


@route
class BoardHandler(BaseHandler):
    async def prepare(self):
        super().prepare()
        if not await self.exists():
            self.write_error(404, f"Board {self.model.BoardId} not found")

    async def load(self):
        cursor = self.db.boards.aggregate(self.model.query)
        await cursor.fetch_next
        return cursor.next_object()

    async def post(self):
        cached = self.cache.get(self.model.id)
        if cached:
            self.log.debug("Cached response")
            self.write(cached)
        else:
            self.write(await self.load())
            pipeline = self.cache.pipeline()
            pipeline.set(self.model.id, b"".join(self._write_buffer))
            pipeline.set(self.model["BoardId"], self.model.id)
            pipeline.execute()

    async def exists(self):
        cached = self.cache.get("boards")
        if cached:
            boards = loads(cached.decode())
        else:
            boards = await self.db.boards.find().distinct("Id")
            self.cache.set("boards", boards)
        return self.model.BoardId in boards
