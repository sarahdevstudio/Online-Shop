from models.order import Order
from utils.file_manager import FileManager
from services.cart_service import CartService
from services.product_service import ProductService


class OrderService:

    ORDERS_FILE = "data/orders.txt"

    @staticmethod
    def get_orders():

        orders = []

        lines = FileManager.read_file(
            OrderService.ORDERS_FILE
        )

        for line in lines:

            line = line.strip()

            if not line:
                continue

            data = line.split("|")

            if len(data) != 5:
                continue

            try:

                order = Order(
                    int(data[0]),
                    int(data[1]),
                    data[2],
                    float(data[3]),
                    data[4]
                )

                orders.append(order)

            except ValueError:
                continue

        return orders

    @staticmethod
    def checkout(user_id):

        carts = CartService.get_user_cart(user_id)

        if not carts:

            return False, "Your cart is empty."

        # بررسی موجودی تمام محصولات
        for cart in carts:

            product = ProductService.get_product_by_id(
                cart.product_id
            )

            if product is None:

                return False, (
                    f"Product {cart.product_id} "
                    "not found."
                )

            if cart.quantity > product.stock:

                return False, (
                    f"Not enough stock for "
                    f"{product.name}."
                )

        # محاسبه مبلغ
        total_price = 0

        product_data = []

        for cart in carts:

            product = ProductService.get_product_by_id(
                cart.product_id
            )

            item_total = (
                product.price * cart.quantity
            )

            total_price += item_total

            product_data.append(
                f"{product.id},{cart.quantity}"
            )

        # ایجاد Order ID
        orders = OrderService.get_orders()

        new_order_id = 1

        if orders:

            new_order_id = max(
                order.order_id
                for order in orders
            ) + 1

        products_string = ";".join(product_data)

        order = Order(
            new_order_id,
            user_id,
            products_string,
            total_price,
            "Pending"
        )

        # ذخیره سفارش
        line = (
            f"{order.order_id}|"
            f"{order.user_id}|"
            f"{order.products}|"
            f"{order.total_price}|"
            f"{order.status}\n"
        )

        FileManager.append_to_file(
            OrderService.ORDERS_FILE,
            line
        )

        # کم کردن موجودی
        ProductService.reduce_stock_for_cart(carts)

        # خالی کردن سبد
        CartService.clear_cart(user_id)

        return True, order

    @staticmethod
    def get_user_orders(user_id):

        orders = OrderService.get_orders()

        user_orders = []

        for order in orders:

            if order.user_id == user_id:

                user_orders.append(order)

        return user_orders

    @staticmethod
    def display_user_orders(user_id):

        orders = OrderService.get_user_orders(
            user_id
        )

        if not orders:

            print("\nYou have no orders.")
            return

        print("\n================ ORDER HISTORY ================")

        for order in orders:

            print(f"""
Order ID   : {order.order_id}
Products   : {order.products}
Total      : {order.total_price}
Status     : {order.status}
--------------------------------------------
""")
