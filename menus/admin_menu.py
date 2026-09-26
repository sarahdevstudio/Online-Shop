from services.product_service import ProductService


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
            add_product_menu()

        elif choice == "2":
            edit_product_menu()

        elif choice == "3":
            delete_product_menu()

        elif choice == "4":
            ProductService.display_products()

        elif choice == "5":
            search_product_menu()

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


def add_product_menu():

    print("\n========== ADD PRODUCT ==========")

    name = input("Product name: ")
    category = input("Category: ")

    try:
        price = float(input("Price: "))
        stock = int(input("Stock: "))
    except ValueError:
        print("Invalid price or stock.")
        return

    if price < 0 or stock < 0:
        print("Price and stock cannot be negative.")
        return

    product = ProductService.add_product(
        name,
        category,
        price,
        stock
    )

    print("\nProduct added successfully!")
    print(f"Product ID: {product.id}")


def edit_product_menu():

    print("\n========== EDIT PRODUCT ==========")

    try:
        product_id = int(input("Product ID: "))
    except ValueError:
        print("Invalid Product ID.")
        return

    product = ProductService.get_product_by_id(product_id)

    if product is None:
        print("Product not found.")
        return

    print("\nCurrent information:")

    print(f"Name: {product.name}")
    print(f"Category: {product.category}")
    print(f"Price: {product.price}")
    print(f"Stock: {product.stock}")

    print("\nEnter new information:")

    name = input("New name: ")
    category = input("New category: ")

    try:
        price = float(input("New price: "))
        stock = int(input("New stock: "))
    except ValueError:
        print("Invalid price or stock.")
        return

    if price < 0 or stock < 0:
        print("Price and stock cannot be negative.")
        return

    success = ProductService.update_product(
        product_id,
        name,
        category,
        price,
        stock
    )

    if success:
        print("Product updated successfully.")
    else:
        print("Product update failed.")


def delete_product_menu():

    print("\n========== DELETE PRODUCT ==========")

    try:
        product_id = int(input("Product ID: "))
    except ValueError:
        print("Invalid Product ID.")
        return

    product = ProductService.get_product_by_id(product_id)

    if product is None:
        print("Product not found.")
        return

    print(f"Product: {product.name}")

    confirm = input("Are you sure? (y/n): ")

    if confirm.lower() != "y":
        print("Delete cancelled.")
        return

    success = ProductService.delete_product(product_id)

    if success:
        print("Product deleted successfully.")
    else:
        print("Product deletion failed.")


def search_product_menu():

    print("\n========== SEARCH PRODUCT ==========")

    search_text = input("Search: ")

    results = ProductService.search_product(search_text)

    ProductService.display_products(results)
