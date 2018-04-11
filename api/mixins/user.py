class UserMixin:
    async def load(self, username):
        query = {"UserName": username, "BoardId": {"$exists": True}}
        async for document in self.db.users.find(query):
            pass
