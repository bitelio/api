class Mock:
    def __init__(self, log):
        self.log = log

    def __getattr__(self, name):
        return self

    def __call__(self, *args, **kwargs):
        self.log.info({"args": args, "kwargs": kwargs})
