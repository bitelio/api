from .auth import AuthMixin
from tornado.web import Finish


class BoardMixin(AuthMixin):
    def prepare(self):
        super().prepare()
        board_id = self.path_kwargs.get("board_id")
        if board_id not in self.user["Boards"]:
            self.write_error(403, "Forbidden")
            raise Finish()
        else:
            self.board_id = int(board_id)
            self.log = self.log.bind(board_id=board_id)

    @property
    def query(self):
        return {"BoardId": self.board_id}
