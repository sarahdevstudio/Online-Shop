from models.product import Product
from utils.file_manager import FileManager


class ProductService:

    PRODUCTS_FILE = "data/products.txt"

    @staticmethod
    def get_products():
        products = []

        lines = FileManager.read_file(ProductService.PRODUCTS_FILE)

        for line in lines:
            line = line.strip()

            if not line:
                continue

            data = line.split("|")

            if len(data) != 5:
                continue

            try:
                product = Product(
                    int(data[0]),
                    data[1],
                    data[2],
                    float(data[3]),
                    int(data[4])
                )

                products.append(product)

            except ValueError:
                continue

        return products

    @staticmethod
    def add_product(name, category, price, stock):
        products = ProductService.get_products()

        new_id = 1

        if products:
            new_id = max(product.id for product in products) + 1

        product = Product(
            new_id,
            name,
            category,
            price,
            stock
        )

        line = (
            f"{product.id}|"
            f"{product.name}|"
            f"{product.category}|"
            f"{product.price}|"
            f"{product.stock}\n"
        )

        FileManager.append_to_file(
            ProductService.PRODUCTS_FILE,
            line
        )

        return product

    @staticmethod
    def update_product(product_id, name, category, price, stock):
        products = ProductService.get_products()

        found = False

        for product in products:

            if product.id == product_id:
                product.name = name
                product.category = category
                product.price = price
                product.stock = stock

                found = True
                break

        if not found:
            return False

        data = []

        for product in products:
            line = (
                f"{product.id}|"
                f"{product.name}|"
                f"{product.category}|"
                f"{product.price}|"
                f"{product.stock}\n"
            )

            data.append(line)

        FileManager.update_file(
            ProductService.PRODUCTS_FILE,
            data
        )

        return True

    @staticmethod
    def delete_product(product_id):
        products = ProductService.get_products()

        new_products = []

        found = False

        for product in products:

            if product.id == product_id:
                found = True
                continue

            new_products.append(product)

        if not found:
            return False

        data = []

        for product in new_products:
            line = (
                f"{product.id}|"
                f"{product.name}|"
                f"{product.category}|"
                f"{product.price}|"
                f"{product.stock}\n"
            )

            data.append(line)

        FileManager.update_file(
            ProductService.PRODUCTS_FILE,
            data
        )

        return True

    @staticmethod
    def search_product(search_text):
        products = ProductService.get_products()

        results = []

        search_text = search_text.lower()

        for product in products:

            if (
                search_text in product.name.lower()
                or search_text in product.category.lower()
            ):
                results.append(product)

        return results

    @staticmethod
    def get_product_by_id(product_id):
        products = ProductService.get_products()

        for product in products:

            if product.id == product_id:
                return product

        return None

    @staticmethod
    def display_products(products=None):

        if products is None:
            products = ProductService.get_products()

        if not products:
            print("\nNo products found.")
            return

        print("\n================ PRODUCTS ================")

        for product in products:

            print(f"""
ID       : {product.id}
Name     : {product.name}
Category : {product.category}
Price    : {product.price}
Stock    : {product.stock}
--------------------------------------------
""")
