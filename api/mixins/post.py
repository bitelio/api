from sys import exc_info
from json import loads
from schematics.exceptions import DataError


class PostMixin:
    def prepare(self):
        super().prepare()
        if self.request.method == "POST":
            try:
                body = loads(self.request.body or "{}")
                self.body = self.model(body, validate=True)
            except DataError as error:
                self.write_error(400, str(error))
            except:
                error = exc_info()[0].__name__
                self.write_error(400, f"Invalid body format: {error}")

    async def post(self):
        data = {"$set": self.body.to_native()}
        status = await self.mongo.users.update_one(self.query, data)
        self.write({"message": status.raw_result})

    def query(self):
        raise NotImplemented
