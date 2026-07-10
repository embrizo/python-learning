import os
import json
from typing import List, Optional
from account import Account

# Resolve the absolute path to account.json
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, "account.json")

# Globally accessible variables in this module, typed correctly
accounts: List[Account] = []
current_account: Optional[Account] = None

def load_accounts() -> List[Account]:
    """Loads accounts from the JSON data file, mapping them to Account objects.

    Returns:
        List of loaded Account instances.
    """
    global accounts
    if not os.path.exists(DATA_FILE):
        return []
    
    with open(DATA_FILE, "r", encoding="utf-8") as file:  
        raw_list = json.load(file)
        # Map dictionary values to Account objects
        accounts = [
            Account(
                username=acc["username"],
                password=acc["password"],
                balance=float(acc["balance"]),
                history=acc["history"]
            )
            for acc in raw_list
        ]
    return accounts

def save_accounts() -> None:
    """Serializes and saves all Account objects back to the JSON data file."""
    with open(DATA_FILE, "w", encoding="utf-8") as file:  
        # Convert Account instances back to dictionary representation for writing
        serialized = [acc.to_dict() for acc in accounts]
        json.dump(serialized, file, indent=4, ensure_ascii=False)

def set_current_account(account: Account) -> None:
    """Sets the active logged-in account context.

    Args:
        account: The Account instance to set as active.
    """
    global current_account
    current_account = account

def get_current_account() -> Optional[Account]:
    """Retrieves the active logged-in account context.

    Returns:
        The current active Account instance or None if not logged in.
    """
    return current_account

def changepass() -> None:
    """Prompts the user to update their password, calling validation and saving state."""
    global current_account
    if current_account is None:
        print("No user logged in.")
        return
    print(f"Your old password is {current_account.password_raw}")
    password = input("Enter your new password: ").strip()
    if not password:
        print("Password cannot be empty.")
        return
    current_account.change_password(password)
    save_accounts()
    print("Change password successful")

# Load accounts initially
accounts = load_accounts()