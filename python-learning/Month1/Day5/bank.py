import storage


def login() -> bool:
    """Prompt the user for credentials and verify them against loaded accounts.

    Returns:
        True if login is successful, False otherwise.
    """
    storage.load_accounts()
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    for acc in storage.accounts:  #...
        if acc.username == username and acc.verify_password(password):
            storage.set_current_account(acc)
            print("Login successful")
            return True

    print("Login failed")
    return False


def show_menu() -> None:
    """Print the ATM operation menu."""
    print("\n--- ATM Menu ---")
    print("1. Deposit")
    print("2. Withdraw")
    print("3. Show Balance")
    print("4. Show History")
    print("5. Transfer")
    print("6. Change Password")
    print("7. Exit")


def check_balance() -> None:
    """Print the balance of the current logged-in account."""
    account = storage.get_current_account()
    if account:
        print(f"Balance: {account.balance}")
    else:
        print("No user logged in.")


def show_history() -> None:
    """Print the transaction history of the current logged-in account."""
    account = storage.get_current_account()
    if account:
        account.print_history()
    else:
        print("No user logged in.")