import storage

def deposit():
    account = storage.get_current_account()
    if not account:
        print("No user logged in.")
        return
    amount = float(input("Enter amount to deposit: "))
    account["balance"] += amount
    account["history"].append(amount)
    storage.save_accounts()
    print("Deposit successful")

def withdraw():
    account = storage.get_current_account()
    if not account:
        print("No user logged in.")
        return
    amount = float(input("Enter amount to withdraw: "))
    if amount > account["balance"]:
        print("Insufficient balance!")
    else:
        account["balance"] -= amount
        account["history"].append(-amount)
        storage.save_accounts()
        print("Withdraw successful")

def transfer():
    account = storage.get_current_account()
    if not account:
        print("No user logged in.")
        return
    
    target_username = input("Enter username of the person you want to transfer to: ")
    amount = float(input("Enter amount to transfer: "))
    
    if amount > account["balance"]:
        print("Insufficient balance!")
        return
        
    # Find the target account
    target_account = None
    for acc in storage.accounts:
        if acc["username"] == target_username:
            target_account = acc
            break
            
    if target_account is None:
        print(f"Target account '{target_username}' not found!")
        return
        
    # Perform transfer
    account["balance"] -= amount
    account["history"].append(-amount)
    
    target_account["balance"] += amount
    target_account["history"].append(amount)
    
    storage.save_accounts()
    print(f"Transfer to {target_username}'s account successful")