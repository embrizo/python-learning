import storage

def show_menu():
    print("1. Deposit")
    print("2. Withdraw")
    print("3. Show Balance")
    print("4. Show History")
    print("5. Transfer")
    print("6. Change Password")
    print("7. Exit")

def check_balance():
    account = storage.get_current_account()
    if account:
        print(f"Balance: {account['balance']}")
    else:
        print("No user logged in.")

def show_history():
    account = storage.get_current_account()
    if account:
        print(f"History: {account['history']}")
    else:
        print("No user logged in.")