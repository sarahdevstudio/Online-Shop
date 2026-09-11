from utils.file_manager import FileManager


file_path = "data/users.txt"


FileManager.write_file(
    file_path,
    [
        "1|ali|1234|Ali|09120000000|Baku|user\n",
        "2|admin|admin123|Admin|09121111111|Baku|admin\n"
    ]
)


users = FileManager.read_file(file_path)

for user in users:
    print(user)
