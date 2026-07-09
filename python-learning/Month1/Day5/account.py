from typing import List

class Account:
    """Represents a bank account with basic operations like deposit, withdraw, and transfer."""

    def __init__(self, username: str, password: str, balance: float, history: List[float]):
        """Initialize a new Account instance.

        Args:
            username: The owner's username.
            password: The account password.
            balance: The initial balance.
            history: The transaction history list.
        """
        self.username: str = username
        self.__password: str = password
        self.__balance: float = balance
        self.history: List[float] = history

    @property
    def balance(self) -> float:
        """Get the current account balance."""
        return self.__balance

    def verify_password(self, password: str) -> bool:
        """Verify if the provided password matches the account password."""
        return self.__password == password

    def change_password(self, new_password: str) -> None:
        """Change the account password."""
        self.__password = new_password

    def deposit(self, amount: float) -> None:
        """Deposit a positive amount into the account.

        Args:
            amount: The amount to deposit.
        """
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.__balance += amount
        self.history.append(amount)

    def withdraw(self, amount: float) -> None:
        """Withdraw a positive amount from the account.

        Args:
            amount: The amount to withdraw.
        """
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.__balance:
            raise ValueError("Insufficient balance.")
        self.__balance -= amount
        self.history.append(-amount)

    def transfer(self, target_account: 'Account', amount: float) -> None:
        """Transfer a positive amount to another Account.

        Args:
            target_account: The destination Account object.
            amount: The amount to transfer.
        """
        if amount <= 0:
            raise ValueError("Transfer amount must be positive.")
        if amount > self.__balance:
            raise ValueError("Insufficient balance for transfer.")
        self.withdraw(amount)
        target_account.deposit(amount)

    def print_history(self) -> None:
        """Print the transaction history of this account."""
        if self.history:
            print(f"Transaction History for {self.username}: {self.history}")
        else:
            print(f"No transaction history for {self.username}.")

    def to_dict(self) -> dict:
        """Convert the Account object back to a dictionary for JSON serialization."""
        return {
            "username": self.username,
            "password": self.__password,
            "balance": self.__balance,
            "history": self.history
        }