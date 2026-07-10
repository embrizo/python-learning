from typing import List

class Account:
    """Represents a bank account with basic transaction methods and state encapsulation."""

    def __init__(self, username: str, password: str, balance: float, history: List[float]):
        """Initializes the account object.

        Args:
            username: User identification name.
            password: Password key.
            balance: Initial cash value of the account.
            history: Transaction ledger entries.
        """
        self.username: str = username
        self.__password: str = password      # Private attribute
        self.__balance: float = balance      # Encapsulated balance (Private attribute)
        self.history: List[float] = history

    @property
    def balance(self) -> float:
        """Getter for the balance attribute.

        Returns:
            The current account balance.
        """
        return self.__balance

    @property
    def password_raw(self) -> str:
        """Getter for the raw password.

        Returns:
            The password string.
        """
        return self.__password

    def verify_password(self, password: str) -> bool:
        """Verifies if the provided password matches the private account password.

        Args:
            password: The password to check.

        Returns:
            True if matched, False otherwise.
        """
        return self.__password == password

    def change_password(self, new_password: str) -> None:
        """Updates the account password key.

        Args:
            new_password: The new password to save.
        """
        self.__password = new_password

    def deposit(self, amount: float) -> None:
        """Performs deposit on the account ledger.

        Args:
            amount: Non-negative value to deposit.

        Raises:
            ValueError: If the amount is less than or equal to 0.
        """
        if amount <= 0:
            raise ValueError("Deposit amount must be greater than zero.")
        self.__balance += amount
        self.history.append(amount)

    def withdraw(self, amount: float) -> None:
        """Performs withdrawal check and updates the ledger.

        Args:
            amount: Non-negative value to withdraw.

        Raises:
            ValueError: If the amount is <= 0 or exceeds the current balance.
        """
        if amount <= 0:
            raise ValueError("Withdrawal amount must be greater than zero.")
        if amount > self.__balance:
            raise ValueError("Insufficient balance!")
        self.__balance -= amount
        self.history.append(-amount)

    def record_transfer_sent(self, amount: float) -> None:
        """Subtracts transfer value and appends negative transaction history.

        Args:
            amount: Non-negative transfer value.

        Raises:
            ValueError: If the amount is <= 0 or exceeds balance.
        """
        if amount <= 0:
            raise ValueError("Transfer amount must be greater than zero.")
        if amount > self.__balance:
            raise ValueError("Insufficient balance!")
        self.__balance -= amount
        self.history.append(-amount)

    def record_transfer_received(self, amount: float) -> None:
        """Adds transfer value and appends positive transaction history.

        Args:
            amount: Non-negative incoming transfer value.

        Raises:
            ValueError: If the amount is <= 0.
        """
        if amount <= 0:
            raise ValueError("Received amount must be greater than zero.")
        self.__balance += amount
        self.history.append(amount)

    def to_dict(self) -> dict:
        """Converts the object fields into a JSON serializable dictionary.

        Returns:
            Dictionary containing public and private account schema attributes.
        """
        return {
            "username": self.username,
            "password": self.__password,
            "balance": self.__balance,
            "history": self.history
        }
