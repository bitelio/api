from json import loads, JSONDecodeError
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
            except JSONDecodeError:
                self.write_error(400, f"Invalid body format")

    async def post(self, *args, **kwargs):
        name = self.collection.replace('_', ' ')
        self.log = self.log.bind(event=f"Updating {name}")
        data = {"$set": self.body.to_native()}
        status = await self.mongo[self.collection].update_one(self.query, data)
        self.write({"message": status.raw_result})

    @staticmethod
    def query(self):
        raise NotImplementedError
