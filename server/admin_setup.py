from db import init_db, add_user

def main():
    init_db()
    print("=== Admin User Setup ===")

    username = input("Username: ").strip()
    password = input("Password: ").strip()
    group = input("Group name: ").strip()

    add_user(username, password, group)
    print("User added successfully")

if __name__ == "__main__":
    main()
