
def admin_menu(user):

    while True:

        print("\n================================")
        print("          ADMIN MENU")
        print("================================")

        print("1. Add Product")
        print("2. Edit Product")
        print("3. Delete Product")
        print("4. View Products")
        print("5. Search Product")
        print("6. View Users")
        print("7. View Orders")
        print("8. Change Order Status")
        print("9. Logout")

        choice = input("Choose an option: ")

        if choice == "1":
            print("Add Product - Coming Soon")

        elif choice == "2":
            print("Edit Product - Coming Soon")

        elif choice == "3":
            print("Delete Product - Coming Soon")

        elif choice == "4":
            print("View Products - Coming Soon")

        elif choice == "5":
            print("Search Product - Coming Soon")

        elif choice == "6":
            print("View Users - Coming Soon")

        elif choice == "7":
            print("View Orders - Coming Soon")

        elif choice == "8":
            print("Change Order Status - Coming Soon")

        elif choice == "9":
            print("Logged out successfully.")
            break

        else:
            print("Invalid option.")
