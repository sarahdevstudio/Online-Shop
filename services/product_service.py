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

            product = Product(
                int(data[0]),
                data[1],
                data[2],
                float(data[3]),
                int(data[4])
            )

            products.append(product)

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
    def display_products():
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
