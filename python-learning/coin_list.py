count = 1

while count <= 5:
    print(count)
    count += 1

for i in range(5):
    print(i)

print(f"________________________")

coins = ["BTC","ETH","SOL","XRP","DOGE"]

for coin in coins:
    print(coin)

print(f"________________________")

nub = 4
while nub >= 0:
    print(f"{coins[nub]}")
    nub -= 1
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

if authen == True:
    print("Welcome to the ATM system")
    while True:
        print("1. Check Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            print(f"Balance: {balance}")
        elif choice == "2":
            depo = float(input("Enter amount to deposit: "))
            balance += depo
            print(f"Balance: {balance}")
        elif choice == "3":
            withdr = float(input("Enter amount to withdraw: "))
            if withdr > balance:
                print("Insufficient balance")
            else:
                balance -= withdr
                print(f"Balance: {balance}")
        elif choice == "4":
            print("Exit Goodbye")
            break
        else:
            print("Invalid choice")