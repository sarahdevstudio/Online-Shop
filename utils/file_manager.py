import os


class FileManager:

    @staticmethod
    def read_file(file_path):

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

        if os.path.exists(file_path):

            os.remove(file_path)
