import hashlib
import hmac
import os


class PasswordHelper:

    ITERATIONS = 100_000

    @staticmethod
    def hash_password(password):

        salt = os.urandom(16).hex()

        digest = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt.encode("utf-8"),
            PasswordHelper.ITERATIONS
        ).hex()

        return f"{salt}${digest}"

    @staticmethod
    def is_legacy_hash(hashed_password):

        # old format: plain unsalted SHA-256
        return "$" not in hashed_password

    @staticmethod
    def verify_password(password, hashed_password):

        if PasswordHelper.is_legacy_hash(hashed_password):

            legacy = hashlib.sha256(
                password.encode("utf-8")
            ).hexdigest()

            return hmac.compare_digest(
                legacy,
                hashed_password
            )

        salt, digest = hashed_password.split("$", 1)

        candidate = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt.encode("utf-8"),
            PasswordHelper.ITERATIONS
        ).hex()

        return hmac.compare_digest(candidate, digest)
