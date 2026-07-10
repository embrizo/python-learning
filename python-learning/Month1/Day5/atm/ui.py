import storage

def show_menu() -> None:
    """Renders the option selection menu to the console."""
    print("1. Deposit")
    print("2. Withdraw")
    print("3. Show Balance")
    print("4. Show History")
    print("5. Transfer")
    print("6. Change Password")
    print("7. Exit")

def check_balance() -> None:
    """Fetches the active Account instance balance and prints it to console."""
    account = storage.get_current_account()
    if account:
        # Access balance via Account property
        print(f"Balance: {account.balance}")
    else:
        print("No user logged in.")

def show_history() -> None:
    """Fetches the active Account instance history and prints it to console."""
    account = storage.get_current_account()
    if account:
        # Access history list via Account attribute
        print(f"History: {account.history}")
    else:
        print("No user logged in.")