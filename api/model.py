class Model:
    def __init__(self, collection, request, db):
        self.collection = collection

    def find(self):
        if isinstance(self.request, dict):
            self.db.find(self.request.query, projection)
        elif isinstance(query, list):
            self.db.aggregate(query)


class Handler:
    collection = "lanes"
    request = BoardRequest
    response = ["Id", "Title"]
