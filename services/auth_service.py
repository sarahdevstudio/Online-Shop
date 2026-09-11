from models.user import User
from utils.file_manager import FileManager


class AuthService:

    USERS_FILE = "data/users.txt"

    @staticmethod
    def get_users():
        users = []

        lines = FileManager.read_file(AuthService.USERS_FILE)

        for line in lines:
            line = line.strip()

            if not line:
                continue

            data = line.split("|")

            if len(data) != 7:
                continue

            user = User(
                int(data[0]),
                data[1],
                data[2],
                data[3],
                data[4],
                data[5],
                data[6]
            )

            users.append(user)

        return users

    @staticmethod
    def register(username, password, name, phone, address):
        users = AuthService.get_users()

        for user in users:
            if user.username == username:
                return False, "Username already exists."

        new_id = 1

        if users:
            new_id = max(user.id for user in users) + 1

        new_user = User(
            new_id,
            username,
            password,
            name,
            phone,
            address,
            "user"
        )

        line = (
            f"{new_user.id}|"
            f"{new_user.username}|"
            f"{new_user.password}|"
            f"{new_user.name}|"
            f"{new_user.phone}|"
            f"{new_user.address}|"
            f"{new_user.role}\n"
        )

        FileManager.append_to_file(
            AuthService.USERS_FILE,
            line
        )

        return True, "Registration successful."

    @staticmethod
    def login(username, password):
        users = AuthService.get_users()

        for user in users:
            if user.username == username and user.password == password:
                return user

        return None
