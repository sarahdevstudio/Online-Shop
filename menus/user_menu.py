from services.product_service import ProductService
from services.category_service import CategoryService
from services.cart_service import CartService
from services.order_service import OrderService
from utils.helpers import InputHelper
from services.discount_service import DiscountService

def user_menu(user):

    while True:

        print("\n================================")
        print("           USER MENU")
        print("================================")

        print("1. View Products")
        print("2. Search Product")
        print("3. View Categories")
        print("4. Add Product to Cart")
        print("5. View Cart")
        print("6. Remove Product from Cart")
        print("7. Checkout")
        print("8. Order History")
        print("9. Logout")

        choice = input("Choose an option: ")

        if choice == "1":

            ProductService.display_products()

        elif choice == "2":

            search_product_menu()

        elif choice == "3":

            CategoryService.display_categories()

        elif choice == "4":

            add_to_cart_menu(user)

        elif choice == "5":

            CartService.display_cart(user.id)

        elif choice == "6":

            remove_from_cart_menu(user)

        elif choice == "7":

            checkout_menu(user)

        elif choice == "8":

            OrderService.display_user_orders(user.id)

        elif choice == "9":

            print("Logged out successfully.")
            break

        else:

            print("Invalid option.")


def search_product_menu():

    print("\n========== SEARCH PRODUCT ==========")

    search_text = input("Search: ")

    results = ProductService.search_product(
        search_text
    )

    ProductService.display_products(results)


def add_to_cart_menu(user):

    print("\n========== ADD TO CART ==========")

    ProductService.display_products()

    product_id = InputHelper.get_positive_integer(
        "\nProduct ID: "
    )

    quantity = InputHelper.get_positive_integer(
        "Quantity: "
    )

    success, message = CartService.add_to_cart(
        user.id,
        product_id,
        quantity
    )

    print(message)


def remove_from_cart_menu(user):

    print("\n========== REMOVE FROM CART ==========")

    CartService.display_cart(user.id)

    try:

        product_id = int(
            input("\nProduct ID: ")
        )

    except ValueError:

        print("Invalid Product ID.")
        return

    success = CartService.remove_from_cart(
        user.id,
        product_id
    )

    if success:

        print("Product removed from cart.")

    else:

        print("Product not found in cart.")

def checkout_menu(user):

    print("\n================ CHECKOUT ================")

    CartService.display_cart(user.id)

    carts = CartService.get_user_cart(user.id)

    if not carts:
        return

    subtotal = CartService.calculate_total(
        user.id
    )

    print(
        f"\nSubtotal: {subtotal}"
    )

    discount_code = ""

    use_discount = input(
        "\nDo you have a discount code? (y/n): "
    ).strip().lower()

    if use_discount == "y":

        discount_code = input(
            "Enter discount code: "
        ).strip()

        success, result = (
            DiscountService.validate_discount(
                discount_code
            )
        )

        if not success:

            print(
                f"\n{result}"
            )

            return

        discount = result

        discount_amount = (
            subtotal * discount.percent / 100
        )

        final_total = (
            subtotal - discount_amount
        )

        print(
            f"\nDiscount: "
            f"{discount.percent}%"
        )

        print(
            f"Discount Amount: "
            f"{discount_amount}"
        )

        print(
            f"Final Price: "
            f"{final_total}"
        )

    else:

        final_total = subtotal

        print(
            f"\nFinal Price: "
            f"{final_total}"
        )

    confirm = input(
        "\nDo you want to place the order? (y/n): "
    ).strip().lower()

    if confirm != "y":

        print(
            "\nCheckout cancelled."
        )

        return

    success, result = OrderService.checkout(
        user.id,
        discount_code
    )

    if success:

        print(
            "\nOrder placed successfully!"
        )

        print(
            f"Order ID: "
            f"{result.order_id}"
        )

        print(
            f"Final Price: "
            f"{result.total_price}"
        )

    else:

        print(
            f"\nCheckout failed: {result}"
        )
