from datetime import datetime

from .post import PostMixin


class EditableMixin(PostMixin):
    def on_finish(self):
        event = {"data": self.payload,
                 "date": datetime.today(),
                 "path": self.request.path}
        self.mongo.history.insert_one(event)
