class BaseTGCallRouter:
    def __init__(self, prefix):
        self.prefix = prefix

    def is_call_match_router(self, call: dict) -> bool:
        return call.data.startswith(self.prefix)
