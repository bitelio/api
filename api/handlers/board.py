import api


@api.route
class BoardHandler(api.handlers.BaseHandler):
    def prepare(self):
        super().prepare()
        if self.model.BoardId not in api.boards:
            self.write_error(404, f"Board {self.model.BoardId} not found")

    async def load(self):
        return await api.db.boards.aggregate(self.model.query).to_list(10)

    async def post(self):
        model_id = self.model.hash
        cached = api.cache.get(model_id)
        if cached:
            self.log.debug("Sending cached data")
            self.write(cached)
        else:
            self.write(await self.load())
            pipeline = api.cache.pipeline()
            pipeline.set(model_id, b"".join(self._write_buffer))
            pipeline.set(self.model["BoardId"], model_id)
            pipeline.execute()
