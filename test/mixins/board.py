from .auth import AuthMixin


class BoardMixin(AuthMixin):
    def test_wrong_board(self):
        response = self.get(self.url.replace("1", "2"))
        assert response.code == 403
