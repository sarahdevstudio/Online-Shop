from services.product_service import ProductService
from services.category_service import CategoryService
from services.cart_service import CartService


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

            print("Checkout - Coming Soon")

        elif choice == "8":

            print("Order History - Coming Soon")

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

    try:

        product_id = int(
            input("\nProduct ID: ")
        )

        quantity = int(
            input("Quantity: ")
        )

    except ValueError:

        print("Invalid Product ID or quantity.")
        return

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
