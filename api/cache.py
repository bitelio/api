from api import db


class Board(dict):
    async def __init__(self):
        boards = await db.settings.find({"Update": True}).to_list()
        self.update({board["Id"]: board["Ignored"] for board in boards})


board = Board()
