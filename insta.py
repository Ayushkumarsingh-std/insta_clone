import sqlite3
import bcrypt

# Database setup
def setup_database():
    with sqlite3.connect("user_data.db") as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)

# Register a user
def register(username, password):
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    try:
        with sqlite3.connect("user_data.db") as conn:
            conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed))
        print("User registered successfully!")
    except sqlite3.IntegrityError:
        print("Error: Username already taken.")

# Login a user
def login(username, password):
    with sqlite3.connect("user_data.db") as conn:
        user = conn.execute("SELECT password FROM users WHERE username = ?", (username,)).fetchone()
        if user and bcrypt.checkpw(password.encode(), user[0].encode()):
            print(f"Welcome back, {username}!")
        else:
            print("Invalid credentials.")

# Main workflow
def main():
    setup_database()
    while True:
        choice = input("\n1. Register\n2. Login\n3. Exit\nChoose an option: ")
        if choice == "1":
            register(input("Username: "), input("Password: "))
        elif choice == "2":
            login(input("Username: "), input("Password: "))
        elif choice == "3":
            print("Exiting. Have a great day!")
            break
        else:
            print("Invalid option. Please try again.")

if _name_ == "_main_":
    main()