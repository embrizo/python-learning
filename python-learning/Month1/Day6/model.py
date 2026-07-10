from __future__ import annotations
from typing import List
from transactions import Transaction


class Account:
    """Domain entity representing a bank account.

    Attributes:
        username (str): The account holder's unique username.
        __password (str): Hashed or plain password (private).
        __balance (float): Current account balance (private).
        history (List[Transaction]): List of all transactions on this account.
    """

    def __init__(self, username: str, password: str, balance: float = 0.0) -> None:
        """Initialise a new Account.

        Args:
            username (str): Unique username for the account holder.
            password (str): Account password.
            balance (float): Opening balance. Defaults to 0.0.
        """
        self.username: str = username
        self.__password: str = password
        self.__balance: float = balance
        self.history: List[Transaction] = []

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def password(self) -> str:
        """Return the account password."""
        return self.__password

    @password.setter
    def password(self, value: str) -> None:
        """Set a new password.

        Args:
            value (str): The new password string.
        """
        self.__password = value

    @property
    def balance(self) -> float:
        """Return the current account balance."""
        return self.__balance

    # ------------------------------------------------------------------
    # Business methods (stubs — logic to be implemented later)
    # ------------------------------------------------------------------

    def deposit(self, amount: float) -> None:
        """Deposit money into the account.

        Args:
            amount (float): Positive amount to add to balance.
        """
        pass

    def withdraw(self, amount: float) -> None:
        """Withdraw money from the account.

        Args:
            amount (float): Positive amount to subtract from balance.
        """
        pass

    def add_transaction(self, transaction: Transaction) -> None:
        """Append a completed Transaction to the account history.

        Args:
            transaction (Transaction): The transaction record to store.
        """
        pass

    # ------------------------------------------------------------------
    # Dunder helpers
    # ------------------------------------------------------------------

    def __str__(self) -> str:
        return f"Account(username={self.username}, balance={self.__balance:.2f})"

    def __repr__(self) -> str:
        return f"Account(username={self.username!r}, balance={self.__balance!r})"
