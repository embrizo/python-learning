#ATM CLI
#====================
# ATM SYSTEM
#1. Check Balance
#2. Deposit
#3. Withdraw
#4. Exit

user = input("Enter your username: ")
password = input("Enter your password: ")

authen = False

if user == "admin" and password == "1234":
    print("Login success")
    authen = True
else:
    print("Login failed")
    authen = False
balance = 10000
history = []

if authen == True:
    print("Welcome to the ATM system")
    while True:
        print("1. Check Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. History")
        print("5. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            print(f"Balance: {balance}")
        elif choice == "2":
            depo = float(input("Enter amount to deposit: "))
            balance += depo
            history.append(f"Deposit: {depo}")
            print(f"Balance: {balance}")
        elif choice == "3":
            withdr = float(input("Enter amount to withdraw: "))
            if withdr > balance:
                print("Insufficient balance")
            else:
                balance -= withdr
                history.append(f"Withdraw: {withdr}")
                print(f"Balance: {balance}")
        elif choice == "4":
            print(f"History: {history}")
        elif choice == "5":
            print("Exit Goodbye")
            break
        else:
            print("Invalid choice")

