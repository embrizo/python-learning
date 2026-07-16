import sys
from repository import JsonRepository
from services import BankService
from exceptions import BankError
from logger import logger

def main() -> None:
    """Bootstrap the application and start the interactive CLI loop."""
    repository = JsonRepository()
    service = BankService(repository)
    
    current_user = None

    while True:
        if current_user is None:
            print("\n=== Simple Bank CLI ===")
            print("1. Register")
            print("2. Login")
            print("3. Exit")
            
            choice = input("Select an option: ").strip()
            
            if choice == "1":
                username = input("Enter new username: ").strip()
                password = input("Enter new password: ").strip()
                try:
                    service.register(username, password)
                    print(f"Success: Account '{username}' created successfully!")
                except BankError as e:
                    print(f"Error: {e.message}")
                except Exception as e:
                    logger.error(f"Unexpected error during registration: {str(e)}")
                    print("Error: An unexpected error occurred.")
            
            elif choice == "2":
                username = input("Username: ").strip()
                password = input("Password: ").strip()
                try:
                    current_user = service.login(username, password)
                    print(f"Welcome back, {current_user.username}!")
                except BankError as e:
                    print(f"Error: {e.message}")
                except Exception as e:
                    logger.error(f"Unexpected error during login: {str(e)}")
                    print("Error: An unexpected error occurred.")
                    
            elif choice == "3":
                print("Goodbye!")
                break
            else:
                print("Invalid option, please try again.")
        else:
            print(f"\n=== User Menu ({current_user.username}) ===")
            print("1. Check Balance")
            print("2. Deposit")
            print("3. Withdraw")
            print("4. Transfer")
            print("5. View Transaction History")
            print("6. Logout")
            
            choice = input("Select an option: ").strip()
            
            if choice == "1":
                try:
                    # Sync with storage
                    updated_user = repository.find_by_username(current_user.username)
                    if updated_user:
                        current_user = updated_user
                    print(f"Your current balance is: ${current_user.balance:,.2f}")
                except Exception as e:
                    logger.error(f"Failed to fetch balance: {str(e)}")
                    print("Error: Could not retrieve balance.")
                    
            elif choice == "2":
                amount_str = input("Enter amount to deposit: ").strip()
                try:
                    amount = float(amount_str)
                    service.deposit(current_user.username, amount)
                    print(f"Success: Deposited ${amount:,.2f} successfully.")
                except ValueError:
                    logger.error(f"Failed deposit input from user '{current_user.username}': '{amount_str}' is not a valid number")
                    print("Error: Please enter a valid number.")
                except BankError as e:
                    print(f"Error: {e.message}")
                except Exception as e:
                    logger.error(f"Unexpected error during deposit: {str(e)}")
                    print("Error: An unexpected error occurred.")
                    
            elif choice == "3":
                amount_str = input("Enter amount to withdraw: ").strip()
                try:
                    amount = float(amount_str)
                    service.withdraw(current_user.username, amount)
                    print(f"Success: Withdrew ${amount:,.2f} successfully.")
                except ValueError:
                    logger.error(f"Failed withdrawal input from user '{current_user.username}': '{amount_str}' is not a valid number")
                    print("Error: Please enter a valid number.")
                except BankError as e:
                    print(f"Error: {e.message}")
                except Exception as e:
                    logger.error(f"Unexpected error during withdrawal: {str(e)}")
                    print("Error: An unexpected error occurred.")
                    
            elif choice == "4":
                target = input("Enter recipient username: ").strip()
                amount_str = input("Enter amount to transfer: ").strip()
                try:
                    amount = float(amount_str)
                    service.transfer(current_user.username, target, amount)
                    print(f"Success: Transferred ${amount:,.2f} to '{target}' successfully.")
                except ValueError:
                    logger.error(f"Failed transfer input from user '{current_user.username}': '{amount_str}' is not a valid number")
                    print("Error: Please enter a valid number.")
                except BankError as e:
                    print(f"Error: {e.message}")
                except Exception as e:
                    logger.error(f"Unexpected error during transfer: {str(e)}")
                    print("Error: An unexpected error occurred.")
                    
            elif choice == "5":
                try:
                    # Sync with storage
                    updated_user = repository.find_by_username(current_user.username)
                    if updated_user:
                        current_user = updated_user
                    print(f"\n--- Transaction History for {current_user.username} ---")
                    if not current_user.history:
                        print("No transactions yet.")
                    else:
                        for tx in current_user.history:
                            print(tx)
                except Exception as e:
                    logger.error(f"Failed to fetch history: {str(e)}")
                    print("Error: Could not retrieve transaction history.")
                    
            elif choice == "6":
                print(f"Logged out from '{current_user.username}'.")
                current_user = None
            else:
                print("Invalid option, please try again.")

if __name__ == "__main__":
    main()
