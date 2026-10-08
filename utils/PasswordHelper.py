import hashlib


class PasswordHelper:

    @staticmethod
    def hash_password(password):

        return hashlib.sha256(
            password.encode("utf-8")
        ).hexdigest()

    @staticmethod
    def verify_password(password, hashed_password):

        password_hash = PasswordHelper.hash_password(
            password
        )

        return password_hash == hashed_password
