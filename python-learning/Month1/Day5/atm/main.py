from auth import login
from ui import show_menu, check_balance, show_history
from banking import deposit, withdraw, transfer
from storage import changepass

def main() -> None:
    """The central application entry point driving the main interactive loop."""
    if login():
        while True:
            show_menu()
            choice = input("Enter your choice: ").strip()
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
                print("Exit. Thank you for using our ATM service!")
                break
            else:
                print("Invalid choice! Please enter a number between 1 and 7.")

if __name__ == "__main__":
    main()