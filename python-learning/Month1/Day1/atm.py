#ATM CLI
#====================
# ATM SYSTEM
#1. Check Balance
#2. Deposit
#3. Withdraw
#4. Exit
balance = 10000
history = []

def check_balance():
    print(f"Balance: {balance:.2f}")

def login():
    user = input("Enter your username: ")
    password = input("Enter your password: ")
    if user == "admin" and password == "1234":
        print("Login success")
        return True
    else:
        print("Login failed")
        return False

def deposit():
    global balance
    deposit_amount = float(input("Enter amount to deposit: "))
    balance += deposit_amount
    history.append(f"Deposit: {deposit_amount}")
    print(f"Balance: {balance:.2f}")

def withdraw():
    global balance
    withdraw_amount = float(input("Enter amount to withdraw: "))
    if withdraw_amount > balance:
        print("Insufficient balance")
    else:
        balance -= withdraw_amount
        history.append(f"Withdraw: {withdraw_amount}")
        print(f"Balance: {balance:.2f}")

def show_history():
    for item in history:
        print(item)


if login():
    print("Welcome to the ATM system")
    while True:
        print("1. Check Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. History")
        print("5. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            check_balance()
        elif choice == "2":
            deposit()
        elif choice == "3":
            withdraw()
        elif choice == "4":
            show_history()
        elif choice == "5":
            print("Exit Goodbye")
            break
        else:
            print("Invalid choice")

