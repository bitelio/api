import officehours


class Calculator:
    def __init__(self, start, close, holidays, timezone):
        self.timer = officehours.Calculator(start, close, holidays)
