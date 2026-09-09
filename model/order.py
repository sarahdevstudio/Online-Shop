class Order:

    def __init__(self, order_id, user_id, products, total_price, status):
        self.order_id = order_id
        self.user_id = user_id
        self.products = products
        self.total_price = total_price
        self.status = status
