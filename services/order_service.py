from models.order import Order
from utils.file_manager import FileManager
from services.cart_service import CartService
from services.product_service import ProductService
from services.discount_service import DiscountService


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

        if len(data) != 7:
            continue

        try:

            order = Order(
                int(data[0]),
                int(data[1]),
                data[2],
                float(data[3]),
                data[4],
                data[5],
                float(data[6])
            )

            orders.append(order)

        except ValueError:
            continue

    return orders
    
    @staticmethod
    def get_order_by_id(order_id):

        orders = OrderService.get_orders()

        for order in orders:

            if order.order_id == order_id:
                return order

        return None

    @staticmethod
    def get_user_orders(user_id):

        orders = OrderService.get_orders()

        user_orders = []

        for order in orders:

            if order.user_id == user_id:
                user_orders.append(order)

        return user_orders
    @staticmethod
    def checkout(user_id, discount_code=""):

    carts = CartService.get_user_cart(user_id)

    if not carts:
        return False, "Cart is empty."

    total = 0

    for cart in carts:

        product = ProductService.get_product_by_id(
            cart.product_id
        )

        if product is None:
            return False, "Product not found."

        if cart.quantity > product.stock:
            return False, (
                f"Not enough stock for "
                f"{product.name}."
            )

        total += product.price * cart.quantity

    discount_amount = 0
    discount = None
    
    # check discount
    if discount_code:

        success, result = (
            DiscountService.validate_discount(
                discount_code
            )
        )

        if not success:
            return False, result

        discount = result

        discount_amount = (
            total * discount.percent / 100
        )

    final_total = total - discount_amount

    orders = OrderService.get_orders()

    new_order_id = 1

    if orders:

        new_order_id = max(
            order.order_id
            for order in orders
        ) + 1

    products_data = []

    for cart in carts:

        products_data.append(
            f"{cart.product_id},{cart.quantity}"
        )

    products_string = ";".join(products_data)

    discount_code_value = ""

    if discount:
        discount_code_value = discount.code

    order = Order(
        new_order_id,
        user_id,
        products_string,
        final_total,
        "Pending",
        discount_code_value,
        discount_amount
    )

    line = (
        f"{order.order_id}|"
        f"{order.user_id}|"
        f"{order.products}|"
        f"{order.total_price}|"
        f"{order.status}|"
        f"{order.discount_code}|"
        f"{order.discount_amount}\n"
    )

    FileManager.append_to_file(
        OrderService.ORDERS_FILE,
        line
    )

    # کاهش موجودی محصولات
    ProductService.reduce_stock_for_cart(
        carts
    )

    # add more usage from discount
    if discount:

        DiscountService.increase_usage(
            discount.id
        )

    #clear checkout
    CartService.clear_cart(user_id)

    return True, order 
    @staticmethod
    def update_order_status(order_id, new_status):

        orders = OrderService.get_orders()

        found = False

        for order in orders:

            if order.order_id == order_id:

                order.status = new_status
                found = True
                break

        if not found:
            return False

        data = []

        for order in orders:

            line = (
                f"{order.order_id}|"
                f"{order.user_id}|"
                f"{order.products}|"
                f"{order.total_price}|"
                f"{order.status}\n"
            )

            data.append(line)

        FileManager.update_file(
            OrderService.ORDERS_FILE,
            data
        )

        return True

    @staticmethod
    def display_all_orders():

    orders = OrderService.get_orders()

    if not orders:

        print("\nNo orders found.")
        return

    print("\n================ ALL ORDERS ================")

    for order in orders:

        print(
            f"""
Order ID        : {order.order_id}
User ID         : {order.user_id}
Products        : {order.products}
Final Price     : {order.total_price}
Status          : {order.status}
Discount Code   : {order.discount_code}
Discount Amount : {order.discount_amount}
--------------------------------------------
"""
        )

    @staticmethod
    def display_order(order_id):

    order = OrderService.get_order_by_id(
        order_id
    )

    if order is None:

        print("\nOrder not found.")
        return

    print("""
================ ORDER DETAILS ================
""")

    print(f"Order ID        : {order.order_id}")
    print(f"User ID         : {order.user_id}")
    print(f"Products        : {order.products}")
    print(f"Final Price     : {order.total_price}")
    print(f"Status          : {order.status}")

    if order.discount_code:

        print(
            f"Discount Code   : "
            f"{order.discount_code}"
        )

        print(
            f"Discount Amount : "
            f"{order.discount_amount}"
        )

    else:

        print("Discount        : None")

    print("-----------------------------------------------")

    @staticmethod
    def display_user_orders(user_id):

    orders = OrderService.get_user_orders(
        user_id
    )

    if not orders:

        print("\nNo orders found.")
        return

    print("\n================ ORDER HISTORY ================")

    for order in orders:

        print(
            f"""
Order ID        : {order.order_id}
Products        : {order.products}
Final Price     : {order.total_price}
Status          : {order.status}
Discount Code   : {order.discount_code}
Discount Amount : {order.discount_amount}
--------------------------------------------
"""
        )
