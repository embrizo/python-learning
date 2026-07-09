from bank import login, show_menu, check_balance, show_history
from banking import deposit, withdraw, transfer
from storage import changepass

def main():
    if login():
        while True:
            show_menu()
            choice = input("Enter your choice: ")
            if choice == "1":
                deposit()
            elif choice == "2":
                withdraw()
            elif choice == "3":
                check_balance()
            elif choice == "4":
                show_history()
            elif choice == "5":
                transfer()
            elif choice == "6":
                changepass()
            elif choice == "7":
                print("Thank you for using the ATM.")
                break

if __name__ == "__main__":
    main()