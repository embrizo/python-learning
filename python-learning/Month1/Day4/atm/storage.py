import os
import json

# Get the directory of the current script to save the json file in the same folder
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, "account.json")

# Globally accessible variables in this module
accounts = []
current_account = None

def load_accounts():
    global accounts
    with open(DATA_FILE) as file:  
        accounts = json.load(file)
    return accounts

def save_accounts():
    with open(DATA_FILE, "w") as file:  
        json.dump(accounts, file, indent=4)

def set_current_account(account):
    global current_account
    current_account = account

def get_current_account():
    return current_account

def changepass():
    global current_account
    if current_account is None:
        print("No user logged in.")
        return
    print(f"Your old password is {current_account['password']}")
    password = input("Enter your new password: ")
    current_account["password"] = password
    save_accounts()
    print("Change password successful")

# Load accounts initially
accounts = load_accounts()