class Order:

    def __init__(
        self,
        order_id,
        user_id,
        products,
        total_price,
        status,
        discount_code="",
        discount_amount=0
    ):
        self.order_id = order_id
        self.user_id = user_id
        self.products = products
        self.total_price = total_price
        self.status = status
        self.discount_code = discount_code
        self.discount_amount = discount_amount
