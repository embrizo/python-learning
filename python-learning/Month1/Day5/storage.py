import os
import json
from typing import List, Optional
from account import Account

# Get the directory of the current script to save the json file in the same folder
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, "account.json")

# Globally accessible variables in this module
accounts: List[Account] = []
current_account: Optional[Account] = None

def load_accounts() -> List[Account]:
    """Load accounts from the JSON file and map them to Account instances."""
    global accounts
    if not os.path.exists(DATA_FILE):
        accounts = []
        return accounts
    
    with open(DATA_FILE, "r") as file:  
        raw_data = json.load(file)
        accounts = []
        for item in raw_data:
            acc = Account(
                username=item["username"],
                password=item["password"],
                balance=float(item["balance"]),
                history=list(item["history"])
            )
            accounts.append(acc)
    return accounts

def save_accounts() -> None:
    """Serialize and save Account objects to the JSON file."""
    with open(DATA_FILE, "w") as file:
        json_data = [acc.to_dict() for acc in accounts]
        json.dump(json_data, file, indent=4)

def set_current_account(account: Account) -> None:
    """Set the currently logged-in account."""
    global current_account
    current_account = account

def get_current_account() -> Optional[Account]:
    """Get the currently logged-in account."""
    global current_account
    return current_account

def changepass() -> None:
    """Prompt the user and change their password using the Account OOP method."""
    global current_account
    if current_account is None:
        print("No user logged in.")
        return
    # Note: password is encapsulated in Account, so we use verify_password and change_password
    # Let's prompt for the new password
    new_password = input("Enter your new password: ")
    if len(new_password) < 8:
        print(f"Error: Password must be at least 8 characters long")
        return
    else:
        current_account.change_password(new_password)
        save_accounts()
        print("Change password successful")
