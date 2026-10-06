from utils.validators import Validator


class InputHelper:

    @staticmethod
    def get_required_input(message):

        while True:

            value = input(message).strip()

            if not Validator.is_empty(value):

                return value

            print("This field cannot be empty.")

    @staticmethod
    def get_positive_integer(message):

        while True:

            value = input(message)

            if Validator.is_positive_integer(value):

                return int(value)

            print(
                "Please enter a positive integer."
            )

    @staticmethod
    def get_non_negative_integer(message):

        while True:

            value = input(message)

            if Validator.is_non_negative_integer(value):

                return int(value)

            print(
                "Please enter zero or a positive integer."
            )

    @staticmethod
    def get_positive_float(message):

        while True:

            value = input(message)

            if Validator.is_positive_number(value):

                return float(value)

            print(
                "Please enter a positive number."
            )

    @staticmethod
    def get_non_negative_float(message):

        while True:

            value = input(message)

            if Validator.is_non_negative_number(value):

                return float(value)

            print(
                "Please enter zero or a positive number."
            )

    @staticmethod
    def get_phone(message):

        while True:

            phone = input(message).strip()

            if Validator.is_valid_phone(phone):

                return phone

            print(
                "Invalid phone number."
            )

    @staticmethod
    def get_username(message):

        while True:

            username = input(message).strip()

            if Validator.is_valid_username(username):

                return username

            print(
                "Username must be at least "
                "3 characters and contain no spaces."
            )

    @staticmethod
    def get_password(message):

        while True:

            password = input(message)

            if Validator.is_valid_password(password):

                return password

            print(
                "Password must be at least 4 characters."
          )
