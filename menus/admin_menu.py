from services.product_service import ProductService
from services.category_service import CategoryService
from services.order_service import OrderService

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
        print("8. Logout")

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
            category_management_menu()

        elif choice == "8":
            print("Logged out successfully.")
            break

        else:
            print("Invalid option.")


def add_product_menu():

    print("\n========== ADD PRODUCT ==========")

    name = input("Product name: ")

    print("\nAvailable Categories:")

    CategoryService.display_categories()

    try:

        category_id = int(
            input("\nCategory ID: ")
        )

    except ValueError:

        print("Invalid Category ID.")
        return

    category = CategoryService.get_category_by_id(
        category_id
    )

    if category is None:

        print("Category not found.")
        return

    try:

        price = float(
            input("Price: ")
        )

        stock = int(
            input("Stock: ")
        )

    except ValueError:

        print("Invalid price or stock.")
        return

    if price < 0 or stock < 0:

        print(
            "Price and stock cannot be negative."
        )

        return

    product = ProductService.add_product(
        name,
        category.name,
        price,
        stock
    )

    print("\nProduct added successfully!")

    print(f"Product ID: {product.id}")
    print(f"Category: {product.category}")

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

def category_management_menu():

    while True:

        print("\n================================")
        print("      CATEGORY MANAGEMENT")
        print("================================")

        print("1. Add Category")
        print("2. View Categories")
        print("3. Delete Category")
        print("4. Back")

        choice = input("Choose an option: ")

        if choice == "1":

            add_category_menu()

        elif choice == "2":

            CategoryService.display_categories()

        elif choice == "3":

            delete_category_menu()

        elif choice == "4":

            break

        else:

            print("Invalid option.")

def delete_category_menu():

    print("\n========== DELETE CATEGORY ==========")

    CategoryService.display_categories()

    try:

        category_id = int(
            input("\nCategory ID: ")
        )

    except ValueError:

        print("Invalid Category ID.")
        return

    category = CategoryService.get_category_by_id(
        category_id
    )

    if category is None:

        print("Category not found.")
        return

    print(f"\nCategory: {category.name}")

    confirm = input(
        "Are you sure? (y/n): "
    )

    if confirm.lower() != "y":

        print("Delete cancelled.")
        return

    success = CategoryService.delete_category(
        category_id
    )

    if success:

        print("Category deleted successfully.")

    else:

        print("Category deletion failed.")

def order_management_menu():

    while True:

        print("\n================================")
        print("        ORDER MANAGEMENT")
        print("================================")

        print("1. View All Orders")
        print("2. View Order Details")
        print("3. Change Order Status")
        print("4. Back")

        choice = input("Choose an option: ")

        if choice == "1":

            OrderService.display_all_orders()

        elif choice == "2":

            view_order_details_menu()

        elif choice == "3":

            change_order_status_menu()

        elif choice == "4":

            break

        else:

            print("Invalid option.")

def view_order_details_menu():

    print("\n========== ORDER DETAILS ==========")

    try:

        order_id = int(
            input("Order ID: ")
        )

    except ValueError:

        print("Invalid Order ID.")
        return

    OrderService.display_order(order_id)

def change_order_status_menu():

    print("\n========== CHANGE ORDER STATUS ==========")

    try:

        order_id = int(
            input("Order ID: ")
        )

    except ValueError:

        print("Invalid Order ID.")
        return

    order = OrderService.get_order_by_id(
        order_id
    )

    if order is None:

        print("Order not found.")
        return

    print(f"\nCurrent Status: {order.status}")

    print("\nAvailable Statuses:")

    print("1. Pending")
    print("2. Processing")
    print("3. Shipped")
    print("4. Completed")
    print("5. Cancelled")

    choice = input(
        "\nChoose new status: "
    )

    statuses = {
        "1": "Pending",
        "2": "Processing",
        "3": "Shipped",
        "4": "Completed",
        "5": "Cancelled"
    }

    if choice not in statuses:

        print("Invalid status.")
        return

    new_status = statuses[choice]

    success = OrderService.update_order_status(
        order_id,
        new_status
    )

    if success:

        print(
            f"\nOrder status changed to "
            f"{new_status}."
        )

    else:

        print("Failed to update order status.")
