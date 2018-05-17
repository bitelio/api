from api.handlers import BaseHandler
from api.mixins import BoardMixin, DocumentMixin, PostMixin


class BoardHandler(BoardMixin, DocumentMixin, PostMixin, BaseHandler):
    collection = "boards"
    response = ["AvailableTags", "Timezone", "Update",
                "OfficeHours", "Holidays"]

    @property
    def query(self):
        return {"Id": self.board_id}
