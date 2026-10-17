from datetime import datetime

from models.inventory_record import InventoryRecord
from utils.file_manager import FileManager


class InventoryService:

    HISTORY_FILE = "data/inventory_history.txt"

    @staticmethod
    def get_records():

        records = []

        lines = FileManager.read_file(
            InventoryService.HISTORY_FILE
        )

        for line in lines:

            line = line.strip()

            if not line:
                continue

            data = line.split("|", 5)

            if len(data) != 6:
                continue

            try:

                record = InventoryRecord(
                    int(data[0]),
                    int(data[1]),
                    int(data[2]),
                    data[3],
                    data[4],
                    data[5]
                )

                records.append(record)

            except ValueError:
                continue

        return records

    @staticmethod
    def add_record(
        product_id,
        change,
        operation,
        note=""
    ):

        records = InventoryService.get_records()

        new_id = 1

        if records:
            new_id = max(
                record.id for record in records
            ) + 1

        created_at = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        record = InventoryRecord(
            new_id,
            product_id,
            change,
            operation,
            note,
            created_at
        )

        line = (
            f"{record.id}|"
            f"{record.product_id}|"
            f"{record.change}|"
            f"{record.operation}|"
            f"{record.note}|"
            f"{record.created_at}\n"
        )

        FileManager.append_to_file(
            InventoryService.HISTORY_FILE,
            line
        )

        return record

    @staticmethod
    def get_product_history(product_id):

        records = InventoryService.get_records()

        return [
            record
            for record in records
            if record.product_id == product_id
        ]

    @staticmethod
    def display_history(product_id=None):

        if product_id is None:
            records = InventoryService.get_records()
        else:
            records = InventoryService.get_product_history(
                product_id
            )

        if not records:
            print("\nNo inventory history found.")
            return

        print("\n========== INVENTORY HISTORY ==========")

        for record in records:

            print(
                f"""
Record ID : {record.id}
Product ID: {record.product_id}
Change    : {record.change:+}
Operation : {record.operation}
Note      : {record.note}
Date      : {record.created_at}
----------------------------------------
"""
            )
