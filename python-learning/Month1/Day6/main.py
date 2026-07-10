from repository import JsonRepository
from services import BankService


def main() -> None:
    """Bootstrap the application and start the interactive CLI loop."""
    # --- Dependency injection -----------------------------------------
    repository = JsonRepository(file_path="account.json")
    service = BankService(repository)

    # --- Interactive menu (stub — logic to be implemented later) ------
    while True:
        print("\n=== Simple Bank CLI ===")
        print("1. Login")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Transfer")
        print("5. Exit")

        choice = input("Select an option: ").strip()

        if choice == "1":
            username = input("Username: ")
            password = input("Password: ")
            print(service.login(username, password))

        elif choice == "2":
            username = input("Username: ")
            amount = float(input("Amount: "))
            print(service.deposit(username, amount))

        elif choice == "3":
            username = input("Username: ")
            amount = float(input("Amount: "))
            print(service.withdraw(username, amount))

        elif choice == "4":
            username = input("From username: ")
            target = input("To username: ")
            amount = float(input("Amount: "))
            print(service.transfer(username, target, amount))

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Invalid option, please try again.")


if __name__ == "__main__":
    main()