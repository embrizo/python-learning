import storage

def login() -> bool:
    """Prompts for credentials, verifies them, and registers session if successful.

    Returns:
        True if login is successful, False otherwise.
    """
    storage.load_accounts()
    username = input("Enter your username: ").strip()
    password = input("Enter your password: ").strip()
    
    for account in storage.accounts:
        # Check username and call verify_password method on the Account object
        if username == account.username and account.verify_password(password):
            storage.set_current_account(account)
            print("Login successful")
            return True
            
    print("Login failed")
    return False