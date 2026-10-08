from models.discount import Discount
from utils.file_manager import FileManager


class DiscountService:

    DISCOUNTS_FILE = "data/discounts.txt"

    @staticmethod
    def get_discounts():

        discounts = []

        lines = FileManager.read_file(
            DiscountService.DISCOUNTS_FILE
        )

        for line in lines:

            line = line.strip()

            if not line:
                continue

            data = line.split("|")

            if len(data) != 6:
                continue

            try:

                discount = Discount(
                    int(data[0]),
                    data[1],
                    float(data[2]),
                    int(data[3]),
                    int(data[4]),
                    int(data[5])
                )

                discounts.append(discount)

            except ValueError:
                continue

        return discounts

    @staticmethod
    def get_discount_by_code(code):

        discounts = DiscountService.get_discounts()

        for discount in discounts:

            if discount.code.lower() == code.lower():
                return discount

        return None

    @staticmethod
    def get_discount_by_id(discount_id):

        discounts = DiscountService.get_discounts()

        for discount in discounts:

            if discount.id == discount_id:
                return discount

        return None

    @staticmethod
    def add_discount(code, percent, max_uses):

        discounts = DiscountService.get_discounts()

        # جلوگیری از کد تکراری
        for discount in discounts:

            if discount.code.lower() == code.lower():
                return False

        new_id = 1

        if discounts:
            new_id = max(
                discount.id
                for discount in discounts
            ) + 1

        discount = Discount(
            new_id,
            code,
            percent,
            max_uses,
            0,
            1
        )

        line = (
            f"{discount.id}|"
            f"{discount.code}|"
            f"{discount.percent}|"
            f"{discount.max_uses}|"
            f"{discount.used_count}|"
            f"{discount.active}\n"
        )

        FileManager.append_to_file(
            DiscountService.DISCOUNTS_FILE,
            line
        )

        return True

    @staticmethod
    def delete_discount(discount_id):

        discounts = DiscountService.get_discounts()

        new_discounts = []
        found = False

        for discount in discounts:

            if discount.id == discount_id:

                found = True
                continue

            new_discounts.append(discount)

        if not found:
            return False

        data = []

        for discount in new_discounts:

            line = (
                f"{discount.id}|"
                f"{discount.code}|"
                f"{discount.percent}|"
                f"{discount.max_uses}|"
                f"{discount.used_count}|"
                f"{discount.active}\n"
            )

            data.append(line)

        FileManager.update_file(
            DiscountService.DISCOUNTS_FILE,
            data
        )

        return True

    @staticmethod
    def validate_discount(code):

        discount = DiscountService.get_discount_by_code(code)

        if discount is None:
            return False, "Discount code not found."

        if discount.active != 1:
            return False, "Discount code is inactive."

        if discount.used_count >= discount.max_uses:
            return False, "Discount code usage limit reached."

        return True, discount

    @staticmethod
    def increase_usage(discount_id):

        discounts = DiscountService.get_discounts()

        found = False

        for discount in discounts:

            if discount.id == discount_id:

                discount.used_count += 1
                found = True
                break

        if not found:
            return False

        data = []

        for discount in discounts:

            line = (
                f"{discount.id}|"
                f"{discount.code}|"
                f"{discount.percent}|"
                f"{discount.max_uses}|"
                f"{discount.used_count}|"
                f"{discount.active}\n"
            )

            data.append(line)

        FileManager.update_file(
            DiscountService.DISCOUNTS_FILE,
            data
        )

        return True

    @staticmethod
    def display_discounts():

        discounts = DiscountService.get_discounts()

        if not discounts:

            print("\nNo discount codes found.")
            return

        print("\n================ DISCOUNTS ================")

        for discount in discounts:

            status = "Active"

            if discount.active != 1:
                status = "Inactive"

            print(
                f"""
ID          : {discount.id}
Code        : {discount.code}
Percent     : {discount.percent}%
Usage       : {discount.used_count}/{discount.max_uses}
Status      : {status}
--------------------------------------------
"""
      )
