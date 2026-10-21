from models.user import User
from utils.file_manager import FileManager
from utils.password_helper import PasswordHelper


class AuthService:

    USERS_FILE = "data/users.txt"

    @staticmethod
    def get_users():

        users = []

        lines = FileManager.read_file(
            AuthService.USERS_FILE
        )

        for line in lines:

            line = line.strip()

            if not line:
                continue

            data = line.split("|")

            if len(data) != 7:
                continue

            try:

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

            except ValueError:
                continue

        return users

    @staticmethod
    def get_user_by_id(user_id):

        users = AuthService.get_users()

        for user in users:

            if user.id == user_id:
                return user

        return None

    @staticmethod
    def get_user_by_username(username):

        users = AuthService.get_users()

        for user in users:

            if user.username.lower() == username.lower():
                return user

        return None

    @staticmethod
    def register(
        username,
        password,
        name,
        phone,
        address
    ):

        users = AuthService.get_users()

        for user in users:

            if user.username.lower() == username.lower():

                return False, "Username already exists."

        new_id = 1

        if users:

            new_id = max(
                user.id
                for user in users
            ) + 1

        hashed_password = PasswordHelper.hash_password(password)

        new_user = User(
            new_id,
            username,
            hashed_password,
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
            if user.username.lower() != username.lower():
                continue
                
            if PasswordHelper.verify_password(
                password,
                user.password
            ):

                if PasswordHelper.is_legacy_hash(user.password):
                    AuthService.upgrade_password_hash(
                        users,
                        user,
                        password
                    )

                return user
                
            return None
                    
        return None


    @staticmethod
    def save_users(users):

        data = []

        for user in users:

            line = (
                f"{user.id}|"
                f"{user.username}|"
                f"{user.password}|"
                f"{user.name}|"
                f"{user.phone}|"
                f"{user.address}|"
                f"{user.role}\n"
            )

            data.append(line)

        FileManager.update_file(
            AuthService.USERS_FILE,
            data
        )

    @staticmethod
    def update_profile(user_id, name, phone, address):

        users = AuthService.get_users()

        for user in users:

            if user.id == user_id:

                user.name = name
                user.phone = phone
                user.address = address

                AuthService.save_users(users)

                return True

        return False

    @staticmethod
    def change_password(user_id, old_password, new_password):

        users = AuthService.get_users()

        for user in users:

            if user.id != user_id:
                continue

            if not PasswordHelper.verify_password(
                old_password,
                user.password
            ):
                return False, "Current password is incorrect."

            user.password = PasswordHelper.hash_password(
                new_password
            )

            AuthService.save_users(users)

            return True, "Password changed successfully."

        return False, "User not found."

    @staticmethod
    def upgrade_password_hash(users, user, password):

        user.password = PasswordHelper.hash_password(
            password
        )

        AuthService.save_users(users)

    @staticmethod
    def search_users(search_text):

        users = AuthService.get_users()

        results = []

        search_text = search_text.lower()

        for user in users:

            if (
                search_text in user.username.lower()
                or search_text in user.name.lower()
                or search_text in user.phone.lower()
            ):

                results.append(user)

        return results

    @staticmethod
    def update_user(
        user_id,
        username,
        name,
        phone,
        address,
        role
    ):

        users = AuthService.get_users()

        target_user = None

        for user in users:

            if user.id == user_id:

                target_user = user
                break

        if target_user is None:
            return False

        # check username is not duplicate
        for user in users:

            if (
                user.id != user_id
                and user.username.lower()
                == username.lower()
            ):

                return False

        # at least one admin must remain
        if target_user.role == "admin" and role != "admin":

            admins = [
                user for user in users
                if user.role == "admin"
            ]

            if len(admins) <= 1:
                return False

        target_user.username = username
        target_user.name = name
        target_user.phone = phone
        target_user.address = address
        target_user.role = role

        data = []

        for user in users:

            line = (
                f"{user.id}|"
                f"{user.username}|"
                f"{user.password}|"
                f"{user.name}|"
                f"{user.phone}|"
                f"{user.address}|"
                f"{user.role}\n"
            )

            data.append(line)

        FileManager.update_file(
            AuthService.USERS_FILE,
            data
        )

        return True

    @staticmethod
    def display_users(users=None):

        if users is None:
            users = AuthService.get_users()

        if not users:

            print("\nNo users found.")
            return

        print("\n================ USERS ================")

        for user in users:

            print(f"""
ID       : {user.id}
Username : {user.username}
Name     : {user.name}
Phone    : {user.phone}
Address  : {user.address}
Role     : {user.role}
--------------------------------------------
""")

    @staticmethod
    def create_admin(
        username,
        password,
        name,
        phone,
        address
    ):

        users = AuthService.get_users()

        for user in users:

            if user.username.lower() == username.lower():

                return False, "Username already exists."

        new_id = 1

        if users:

            new_id = max(
                user.id
                for user in users
            ) + 1

        hashed_password = PasswordHelper.hash_password(
            password
        )

        admin = User(
            new_id,
            username,
            hashed_password,
            name,
            phone,
            address,
            "admin"
        )

        line = (
            f"{admin.id}|"
            f"{admin.username}|"
            f"{admin.password}|"
            f"{admin.name}|"
            f"{admin.phone}|"
            f"{admin.address}|"
            f"{admin.role}\n"
        )

        FileManager.append_to_file(
            AuthService.USERS_FILE,
            line
        )

        return True, "Admin created successfully."
