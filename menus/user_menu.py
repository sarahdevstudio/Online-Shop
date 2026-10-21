from services.product_service import ProductService
from services.category_service import CategoryService
from services.cart_service import CartService
from services.order_service import OrderService
from utils.helpers import InputHelper
from services.discount_service import DiscountService
from services.auth_service import AuthService
from services.review_service import ReviewService

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
        print("9. My Profile")
        print("10. Product Reviews")
        print("11. Logout")

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

            profile_menu(user)

        elif choice == "10":

            reviews_menu(user)

        elif choice == "11":

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


def profile_menu(user):

    while True:

        print("\n================================")
        print("          MY PROFILE")
        print("================================")

        print(f"Username : {user.username}")
        print(f"Name     : {user.name}")
        print(f"Phone    : {user.phone}")
        print(f"Address  : {user.address}")

        print("\n1. Edit Profile")
        print("2. Change Password")
        print("3. Back")

        choice = input("Choose an option: ").strip()

        if choice == "1":

            edit_profile_menu(user)

        elif choice == "2":

            change_password_menu(user)

        elif choice == "3":

            break

        else:

            print("Invalid option.")


def edit_profile_menu(user):

    print("\n========== EDIT PROFILE ==========")

    name = InputHelper.get_required_input("New name: ")
    phone = InputHelper.get_phone("New phone: ")
    address = InputHelper.get_required_input("New address: ")

    if AuthService.update_profile(
        user.id,
        name,
        phone,
        address
    ):

        # keep the logged-in session in sync
        user.name = name
        user.phone = phone
        user.address = address

        print("Profile updated successfully.")

    else:

        print("Failed to update profile.")


def change_password_menu(user):

    print("\n========== CHANGE PASSWORD ==========")

    old_password = input("Current password: ")

    new_password = InputHelper.get_password("New password: ")

    confirm = input("Confirm new password: ")

    if new_password != confirm:

        print("Passwords do not match.")
        return

    success, message = AuthService.change_password(
        user.id,
        old_password,
        new_password
    )

    print(message)


def reviews_menu(user):

    while True:

        print("\n================================")
        print("        PRODUCT REVIEWS")
        print("================================")

        print("1. View Product Reviews")
        print("2. Write a Review")
        print("3. Back")

        choice = input("Choose an option: ").strip()

        if choice == "1":

            product_id = InputHelper.get_positive_integer(
                "Product ID: "
            )

            if ProductService.get_product_by_id(product_id) is None:

                print("Product not found.")
                continue

            ReviewService.display_product_reviews(product_id)

        elif choice == "2":

            write_review_menu(user)

        elif choice == "3":

            break

        else:

            print("Invalid option.")


def write_review_menu(user):

    print("\n========== WRITE A REVIEW ==========")

    product_id = InputHelper.get_positive_integer("Product ID: ")

    product = ProductService.get_product_by_id(product_id)

    if product is None:

        print("Product not found.")
        return

    if not ReviewService.has_purchased(user.id, product_id):

        print(
            "You can only review products from "
            "your completed orders."
        )
        return

    while True:

        rating = InputHelper.get_positive_integer(
            "Rating (1-5): "
        )

        if (
            ReviewService.MIN_RATING
            <= rating
            <= ReviewService.MAX_RATING
        ):
            break

        print("Rating must be between 1 and 5.")

    comment = input("Comment (optional): ").strip()

    comment = comment.replace("|", "/")

    success, message = ReviewService.add_review(
        user.id,
        product_id,
        rating,
        comment
    )

    print(message)
