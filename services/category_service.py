from models.category import Category
from utils.file_manager import FileManager


class CategoryService:

    CATEGORIES_FILE = "data/categories.txt"

    @staticmethod
    def get_categories():

        categories = []

        lines = FileManager.read_file(
            CategoryService.CATEGORIES_FILE
        )

        for line in lines:

            line = line.strip()

            if not line:
                continue

            data = line.split("|")

            if len(data) != 2:
                continue

            try:

                category = Category(
                    int(data[0]),
                    data[1]
                )

                categories.append(category)

            except ValueError:
                continue

        return categories

    @staticmethod
    def add_category(name):

        categories = CategoryService.get_categories()

        # جلوگیری از دسته‌بندی تکراری
        for category in categories:

            if category.name.lower() == name.lower():
                return False, None

        new_id = 1

        if categories:
            new_id = max(
                category.id
                for category in categories
            ) + 1

        category = Category(
            new_id,
            name
        )

        line = f"{category.id}|{category.name}\n"

        FileManager.append_to_file(
            CategoryService.CATEGORIES_FILE,
            line
        )

        return True, category

    @staticmethod
    def get_category_by_id(category_id):

        categories = CategoryService.get_categories()

        for category in categories:

            if category.id == category_id:
                return category

        return None

    @staticmethod
    def delete_category(category_id):

        categories = CategoryService.get_categories()

        found = False
        new_categories = []

        for category in categories:

            if category.id == category_id:

                found = True
                continue

            new_categories.append(category)

        if not found:
            return False

        data = []

        for category in new_categories:

            line = (
                f"{category.id}|"
                f"{category.name}\n"
            )

            data.append(line)

        FileManager.update_file(
            CategoryService.CATEGORIES_FILE,
            data
        )

        return True

    @staticmethod
    def display_categories():

        categories = CategoryService.get_categories()

        if not categories:

            print("\nNo categories found.")
            return

        print("\n================ CATEGORIES ================")

        for category in categories:

            print(
                f"ID: {category.id} | "
                f"Name: {category.name}"
            )
