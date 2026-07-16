from __future__ import annotations
from typing import List
from transactions import Transaction
from exceptions import InvalidAmountError, InsufficientBalanceError

class Account:
    """Domain entity representing a bank account with safety checks."""

    def __init__(self, username: str, password: str, balance: float = 0.0) -> None:
        self.username: str = username
        self.__password: str = password
        self.__balance: float = balance
        self.history: List[Transaction] = []

    @property
    def password(self) -> str:
        """Return the account password."""
        return self.__password

    @password.setter
    def password(self, value: str) -> None:
        """Set a new password."""
        self.__password = value

    @property
    def balance(self) -> float:
        """Return the current account balance."""
        return self.__balance

    def deposit(self, amount: float) -> None:
        """Deposit money into the account.

        Raises:
            InvalidAmountError: If amount is negative or zero.
        """
        if amount <= 0:
            raise InvalidAmountError("Deposit amount must be positive.")
        self.__balance += amount

    def withdraw(self, amount: float) -> None:
        """Withdraw money from the account.

        Raises:
            InvalidAmountError: If amount is negative or zero.
            InsufficientBalanceError: If amount exceeds current balance.
        """
        if amount <= 0:
            raise InvalidAmountError("Withdrawal amount must be positive.")
        if amount > self.__balance:
            raise InsufficientBalanceError(
                f"Insufficient balance. Cannot withdraw {amount:.2f} from {self.__balance:.2f}."
            )
        self.__balance -= amount

    def add_transaction(self, transaction: Transaction) -> None:
        """Append a completed Transaction to the account history."""
        self.history.append(transaction)

    def __str__(self) -> str:
        return f"Account(username={self.username}, balance={self.__balance:.2f})"

    def __repr__(self) -> str:
        return f"Account(username={self.username!r}, balance={self.__balance!r})"
