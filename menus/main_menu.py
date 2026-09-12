from services.auth_service import AuthService


def register_menu():
    print("\n========== REGISTER ==========")

    username = input("Username: ")
    password = input("Password: ")
    name = input("Name: ")
    phone = input("Phone: ")
    address = input("Address: ")

    success, message = AuthService.register(
        username,
        password,
        name,
        phone,
        address
    )

    print(message)


def login_menu():
    print("\n========== LOGIN ==========")

    username = input("Username: ")
    password = input("Password: ")

    user = AuthService.login(username, password)

    if user is None:
        print("Invalid username or password.")
        return

    print(f"\nWelcome {user.name}!")

    if user.role == "admin":
        print("You are logged in as Admin.")
    else:
        print("You are logged in as User.")


def main_menu():
    while True:

        print("\n================================")
        print("          ONLINE SHOP")
        print("================================")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            register_menu()

        elif choice == "2":
            login_menu()

        elif choice == "3":
            print("Goodbye!")
            break

        else:
            print("Invalid option.")
