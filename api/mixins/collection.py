from .query import QueryMixin


class CollectionMixin(QueryMixin):
    async def get(self, board_id):
        event = f"Reading {self.collection.replace('_', ' ')}"
        self.log = self.log.bind(event=event)
        cursor = self.db.find(self.query, self.projection)
        self.write(await cursor.to_list(None))
