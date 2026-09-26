from services.product_service import ProductService


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
        print("6. Checkout")
        print("7. Order History")
        print("8. Logout")

        choice = input("Choose an option: ")

        if choice == "1":
            ProductService.display_products()

        elif choice == "2":
            print("Search Product - Coming Soon")

        elif choice == "3":
            print("View Categories - Coming Soon")

        elif choice == "4":
            print("Add Product to Cart - Coming Soon")

        elif choice == "5":
            print("View Cart - Coming Soon")

        elif choice == "6":
            print("Checkout - Coming Soon")

        elif choice == "7":
            print("Order History - Coming Soon")

        elif choice == "8":
            print("Logged out successfully.")
            break

        else:
            print("Invalid option.")
