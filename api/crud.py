class CRUD:
    def __init__(self, db, collection, query):
        self.db = db[collection]
        self.query = query

    async def find(self):
        self.db.find(self.query.query, self.query.projection)

    async def aggregate(self):
        cursor = self.db.aggregate(self.model.query, self.model.projection)
        await cursor.fetch_next
        return cursor.next_object()
