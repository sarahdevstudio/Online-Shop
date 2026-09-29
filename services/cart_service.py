from models.cart import Cart
from utils.file_manager import FileManager
from services.product_service import ProductService


class CartService:

    CARTS_FILE = "data/carts.txt"

    @staticmethod
    def get_carts():

        carts = []

        lines = FileManager.read_file(
            CartService.CARTS_FILE
        )

        for line in lines:

            line = line.strip()

            if not line:
                continue

            data = line.split("|")

            if len(data) != 3:
                continue

            try:

                cart = Cart(
                    int(data[0]),
                    int(data[1]),
                    int(data[2])
                )

                carts.append(cart)

            except ValueError:
                continue

        return carts

    @staticmethod
    def get_user_cart(user_id):

        carts = CartService.get_carts()

        user_cart = []

        for cart in carts:

            if cart.user_id == user_id:
                user_cart.append(cart)

        return user_cart

    @staticmethod
    def add_to_cart(user_id, product_id, quantity):

        product = ProductService.get_product_by_id(
            product_id
        )

        if product is None:
            return False, "Product not found."

        if quantity <= 0:
            return False, "Quantity must be greater than zero."

        if quantity > product.stock:
            return False, "Not enough stock."

        carts = CartService.get_carts()

        # بررسی اینکه محصول قبلاً در سبد هست یا نه
        for cart in carts:

            if (
                cart.user_id == user_id
                and cart.product_id == product_id
            ):

                new_quantity = cart.quantity + quantity

                if new_quantity > product.stock:
                    return False, "Not enough stock."

                cart.quantity = new_quantity

                CartService.save_carts(carts)

                return True, "Product quantity updated."

        # محصول جدید
        new_cart = Cart(
            user_id,
            product_id,
            quantity
        )

        carts.append(new_cart)

        CartService.save_carts(carts)

        return True, "Product added to cart."

    @staticmethod
    def remove_from_cart(user_id, product_id):

        carts = CartService.get_carts()

        new_carts = []

        found = False

        for cart in carts:

            if (
                cart.user_id == user_id
                and cart.product_id == product_id
            ):

                found = True
                continue

            new_carts.append(cart)

        if not found:
            return False

        CartService.save_carts(new_carts)

        return True

    @staticmethod
    def save_carts(carts):

        data = []

        for cart in carts:

            line = (
                f"{cart.user_id}|"
                f"{cart.product_id}|"
                f"{cart.quantity}\n"
            )

            data.append(line)

        FileManager.update_file(
            CartService.CARTS_FILE,
            data
        )

    @staticmethod
    def calculate_total(user_id):

        carts = CartService.get_user_cart(user_id)

        total = 0

        for cart in carts:

            product = ProductService.get_product_by_id(
                cart.product_id
            )

            if product is None:
                continue

            total += product.price * cart.quantity

        return total

    @staticmethod
    def display_cart(user_id):

        carts = CartService.get_user_cart(user_id)

        if not carts:

            print("\nYour cart is empty.")
            return

        print("\n================ YOUR CART ================")

        total = 0

        for cart in carts:

            product = ProductService.get_product_by_id(
                cart.product_id
            )

            if product is None:
                continue

            item_total = product.price * cart.quantity

            total += item_total

            print(f"""
Product ID : {product.id}
Name       : {product.name}
Price      : {product.price}
Quantity   : {cart.quantity}
Total      : {item_total}
--------------------------------------------
""")

        print(f"Cart Total: {total}")
