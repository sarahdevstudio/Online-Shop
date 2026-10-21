import os


class FileManager:

    BASE_DIR = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )

    @staticmethod
    def resolve(file_path):

        if os.path.isabs(file_path):
            return file_path

        return os.path.join(
            FileManager.BASE_DIR,
            file_path
        )

    @staticmethod
    def read_file(file_path):

        file_path = FileManager.resolve(file_path)

        if not os.path.exists(file_path):

            return []

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            return file.readlines()

    @staticmethod
    def write_file(file_path, data):

        file_path = FileManager.resolve(file_path)

        directory = os.path.dirname(file_path)

        if directory:

            os.makedirs(
                directory,
                exist_ok=True
            )

        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as file:

            file.writelines(data)

    @staticmethod
    def append_to_file(file_path, data):

        file_path = FileManager.resolve(file_path)

        directory = os.path.dirname(file_path)

        if directory:

            os.makedirs(
                directory,
                exist_ok=True
            )

        with open(
            file_path,
            "a",
            encoding="utf-8"
        ) as file:

            file.write(data)

    @staticmethod
    def update_file(file_path, data):

        FileManager.write_file(
            file_path,
            data
        )

    @staticmethod
    def delete_file(file_path):

        file_path = FileManager.resolve(file_path)

        if os.path.exists(file_path):

            os.remove(file_path)
