from services.order_service import OrderService
from services.product_service import ProductService


class ReportService:

    LOW_STOCK_THRESHOLD = 5
    TOP_PRODUCTS_COUNT = 5

    @staticmethod
    def parse_order_items(order):

        items = []

        for item in order.products.split(";"):

            try:

                product_id, quantity = item.split(",")

                items.append((int(product_id), int(quantity)))

            except ValueError:
                continue

        return items

    @staticmethod
    def build_report():

        orders = OrderService.get_orders()
        products = ProductService.get_products()

        products_by_id = {
            product.id: product
            for product in products
        }

        status_counts = {}
        revenue = 0
        discounts_given = 0
        units_by_product = {}
        units_by_category = {}

        for order in orders:

            status_counts[order.status] = (
                status_counts.get(order.status, 0) + 1
            )

            # cancelled orders are not real sales
            if order.status == "Cancelled":
                continue

            revenue += order.total_price
            discounts_given += order.discount_amount

            for product_id, quantity in (
                ReportService.parse_order_items(order)
            ):

                units_by_product[product_id] = (
                    units_by_product.get(product_id, 0)
                    + quantity
                )

                product = products_by_id.get(product_id)

                category = (
                    product.category
                    if product
                    else "Deleted products"
                )

                units_by_category[category] = (
                    units_by_category.get(category, 0)
                    + quantity
                )

        top_products = sorted(
            units_by_product.items(),
            key=lambda pair: pair[1],
            reverse=True
        )[:ReportService.TOP_PRODUCTS_COUNT]

        low_stock = [
            product
            for product in products
            if product.stock <= ReportService.LOW_STOCK_THRESHOLD
        ]

        return {
            "total_orders": len(orders),
            "status_counts": status_counts,
            "revenue": revenue,
            "discounts_given": discounts_given,
            "top_products": top_products,
            "units_by_category": units_by_category,
            "low_stock": low_stock,
            "products_by_id": products_by_id
        }

    @staticmethod
    def display_report():

        report = ReportService.build_report()

        print("\n================ SALES REPORT ================")

        print(f"Total orders     : {report['total_orders']}")
        print(f"Revenue          : {report['revenue']}")
        print(f"Discounts given  : {report['discounts_given']}")
        print("(cancelled orders are excluded from revenue)")

        print("\n--- Orders by status ---")

        if not report["status_counts"]:
            print("No orders yet.")

        for status, count in report["status_counts"].items():
            print(f"{status:<12}: {count}")

        print("\n--- Top selling products (units) ---")

        if not report["top_products"]:
            print("No sales yet.")

        for product_id, units in report["top_products"]:

            product = report["products_by_id"].get(product_id)

            name = (
                product.name
                if product
                else f"Deleted product #{product_id}"
            )

            print(f"{name:<20}: {units}")

        print("\n--- Units sold by category ---")

        if not report["units_by_category"]:
            print("No sales yet.")

        for category, units in report["units_by_category"].items():
            print(f"{category:<20}: {units}")

        print(
            f"\n--- Low stock "
            f"(<= {ReportService.LOW_STOCK_THRESHOLD}) ---"
        )

        if not report["low_stock"]:
            print("All products are sufficiently stocked.")

        for product in report["low_stock"]:

            print(
                f"#{product.id} {product.name}: "
                f"{product.stock} left"
            )
