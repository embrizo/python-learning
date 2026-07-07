import os
import json

# Get the directory of the current script to save the json file in the same folder
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, "account.json")

# Default account data
default_account = {
    "username": "Admin",
    "password": "1234",
    "balance": 5000.0,
    "history": []
}

def load_account():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            pass
    return default_account.copy()

def save_account():
    with open(DATA_FILE, "w") as file:
        json.dump(account, file, indent=4)

def login():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    if username == account["username"] and password == account["password"]:
        print("Login successful")
        return True
    else:
        print("Login failed")
        return False

def show_menu():
    print("1. Deposit")
    print("2. Withdraw")
    print("3. Show Balance")
    print("4. Show History")
    print("5. Transfer")
    print("6. Change Password")
    print("7. Exit")

def check_balance():
    print(f"Balance: {account['balance']}")

def show_history():
    print(f"History: {account['history']}")

def deposit():
    amount = float(input("Enter amount to deposit: "))
    account["balance"] += amount
    account["history"].append(amount)
    save_account()
    print("Deposit successful")

def withdraw():
    amount = float(input("Enter amount to withdraw: "))
    if amount > account["balance"]:
        print("Insufficient balance!")
    else:
        account["balance"] -= amount
        account["history"].append(-amount)
        save_account()
        print("Withdraw successful")

def transfer():
    username = input("Enter username of the person you want to transfer to: ")
    amount = float(input("Enter amount to transfer: "))
    if amount > account["balance"]:
        print("Insufficient balance!")
    else:
        account["balance"] -= amount
        account["history"].append(-amount)
        save_account()
        print(f"Transfer to {username}'s account successful")

def change_password():
    print(f"Current password: {account['password']}")
    new_password = input("Enter new password: ")
    account["password"] = new_password
    save_account()
    print("Password changed successfully")

def main():
    if login():
        while True:
            show_menu()
            choice = input("Enter your choice: ")
            if choice == "1":
                deposit()
            elif choice == "2":
                withdraw()
            elif choice == "3":
                check_balance()
            elif choice == "4":
                show_history()
            elif choice == "5":
                transfer()
            elif choice == "6":
                change_password()
            elif choice == "7":
                break

account = load_account()
main()