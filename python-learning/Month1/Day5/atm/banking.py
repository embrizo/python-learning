import storage

def get_valid_amount(prompt: str) -> float:
    """Helper function to prompt and validate numeric float input.

    Loops until a valid float is entered.
    """
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input! Please enter a valid decimal number.")

def deposit() -> None:
    """Handles deposit operation by calling the Account instance deposit method."""
    account = storage.get_current_account()
    if not account:
        print("No user logged in.")
        return

    amount = get_valid_amount("Enter amount to deposit: ")
    try:
        account.deposit(amount)
        storage.save_accounts()
        print("Deposit successful")
    except ValueError as err:
        print(f"Transaction failed: {err}")

def withdraw() -> None:
    """Handles withdraw operation by calling the Account instance withdraw method."""
    account = storage.get_current_account()
    if not account:
        print("No user logged in.")
        return

    amount = get_valid_amount("Enter amount to withdraw: ")
    try:
        account.withdraw(amount)
        storage.save_accounts()
        print("Withdraw successful")
    except ValueError as err:
        print(f"Transaction failed: {err}")

def transfer() -> None:
    """Handles balance transfers between the logged-in user and a target account."""
    account = storage.get_current_account()
    if not account:
        print("No user logged in.")
        return
    
    target_username = input("Enter username of the person you want to transfer to: ").strip()
    if target_username == account.username:
        print("You cannot transfer money to yourself!")
        return

    amount = get_valid_amount("Enter amount to transfer: ")
    
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
        # Perform transactional updates using Account methods
        account.record_transfer_sent(amount)
        target_account.record_transfer_received(amount)
        
        storage.save_accounts()
        print(f"Transfer to {target_username}'s account successful")
    except ValueError as err:
        print(f"Transaction failed: {err}")