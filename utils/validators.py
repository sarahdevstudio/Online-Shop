class Validator:

    @staticmethod
    def is_empty(value):
        return not value or not value.strip()

    @staticmethod
    def is_positive_number(value):

        try:
            number = float(value)

            return number > 0

        except ValueError:
            return False

    @staticmethod
    def is_non_negative_number(value):

        try:
            number = float(value)

            return number >= 0

        except ValueError:
            return False

    @staticmethod
    def is_positive_integer(value):

        try:
            number = int(value)

            return number > 0

        except ValueError:
            return False

    @staticmethod
    def is_non_negative_integer(value):

        try:
            number = int(value)

            return number >= 0

        except ValueError:
            return False

    @staticmethod
    def is_valid_phone(phone):

        phone = phone.strip()

        if not phone:
            return False

        # فقط اعداد و + را قبول می‌کنیم
        allowed_characters = "+0123456789"

        for char in phone:

            if char not in allowed_characters:
                return False

        digits = phone.replace("+", "")

        if not digits.isdigit():
            return False

        if len(digits) < 8 or len(digits) > 15:
            return False

        return True

    @staticmethod
    def is_valid_username(username):

        username = username.strip()

        if len(username) < 3:
            return False

        if " " in username:
            return False

        return True

    @staticmethod
    def is_valid_password(password):

        return len(password) >= 4
