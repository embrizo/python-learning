import storage

def deposit() -> None:
    """Deposit money into the current logged-in account."""
    account = storage.get_current_account()
    if not account:
        print("No user logged in.")
        return
    try:
        amount = float(input("Enter amount to deposit: "))
        account.deposit(amount)
        storage.save_accounts()
        print("Deposit successful")
    except ValueError as e:
        print(f"Error: {e}")

def withdraw() -> None:
    """Withdraw money from the current logged-in account."""
    account = storage.get_current_account()
    if not account:
        print("No user logged in.")
        return
    try:
        amount = float(input("Enter amount to withdraw: "))
        account.withdraw(amount)
        storage.save_accounts()
        print("Withdraw successful")
    except ValueError as e:
        print(f"Error: {e}")

def transfer() -> None:
    """Transfer money from the current logged-in account to another account."""
    account = storage.get_current_account()
    if not account:
        print("No user logged in.")
        return
    
    target_username = input("Enter username of the person you want to transfer to: ")
    try:
        amount = float(input("Enter amount to transfer: "))
    except ValueError:
        print("Error: Invalid amount format.")
        return
        
    # Find the target account
    target_account = None
    for acc in storage.accounts:
        if acc.username == target_username:
            target_account = acc
            break
            
    if target_account is None:
        print(f"Target account '{target_username}' not found!")
        return
        
    try:
        account.transfer(target_account, amount)
        storage.save_accounts()
        print(f"Transfer to {target_username}'s account successful")
    except ValueError as e:
        print(f"Error: {e}")
