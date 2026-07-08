import storage

def login():
    storage.load_accounts()
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    
    for account in storage.accounts:
        if username == account["username"] and password == account["password"]:
            storage.set_current_account(account)
            print("Login successful")
            return True
            
    print("Login failed")
    return False