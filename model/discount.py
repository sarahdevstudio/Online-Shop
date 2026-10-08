class Discount:

    def __init__(
        self,
        id,
        code,
        percent,
        max_uses,
        used_count,
        active
    ):
        self.id = id
        self.code = code
        self.percent = percent
        self.max_uses = max_uses
        self.used_count = used_count
        self.active = active
