from services.product_service import ProductService
from services.category_service import CategoryService
from services.cart_service import CartService
from services.order_service import OrderService
from utils.helpers import InputHelper

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

    print("\n========== CHECKOUT ==========")

    CartService.display_cart(user.id)

    carts = CartService.get_user_cart(user.id)

    if not carts:

        return

    total = CartService.calculate_total(
        user.id
    )

    print(f"\nFinal Total: {total}")

    confirm = input(
        "Do you want to place the order? (y/n): "
    )

    if confirm.lower() != "y":

        print("Checkout cancelled.")
        return

    success, result = OrderService.checkout(
        user.id
    )

    if not success:

        print(result)
        return

    print("\nOrder placed successfully!")

    print(f"Order ID: {result.order_id}")
    print(f"Total Price: {result.total_price}")
    print(f"Status: {result.status}")
