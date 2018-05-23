from api.models import BoardModel
from api.handlers import BaseHandler
from api.mixins import BoardMixin, DocumentMixin, PostMixin


class BoardHandler(BoardMixin, DocumentMixin, PostMixin, BaseHandler):
    model = BoardModel
    collection = "boards"
    response = ["AvailableTags", "Timezone", "Update",
                "OfficeHours", "Holidays", "Id"]

    @property
    def query(self):
        return {"Id": self.board_id}
