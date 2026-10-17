class InventoryRecord:

    def __init__(
        self,
        id,
        product_id,
        change,
        operation,
        note,
        created_at
    ):
        self.id = id
        self.product_id = product_id
        self.change = change
        self.operation = operation
        self.note = note
        self.created_at = created_at
