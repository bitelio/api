class AuthMixin:
    cookie = {"token": "xxx"}

    def get(self, url=None, **kwargs):
        if "Cookie" not in kwargs.get("headers", {}):
            kwargs["headers"] = {"Cookie": "token=xxx"}
        return self.fetch(url or self.url, **kwargs)

    def test_wrong_token(self):
        response = self.get(headers={"Cookie": "token=ooo"})
        assert response.code == 401

    def test_without_token(self):
        response = self.get(headers={"Cookie": ""})
        assert response.code == 401
