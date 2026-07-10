from __future__ import annotations
from typing import Optional

from interfaces import AccountRepositoryInterface
from model import Account
from transactions import Transaction


class BankService:
    """Business-logic layer for banking operations.

    BankService depends on the *AccountRepositoryInterface* abstraction,
    not on any concrete storage class — this follows the
    Dependency Inversion Principle (DIP).

    Args:
        repository (AccountRepositoryInterface): Injected repository.
    """

    def __init__(self, repository: AccountRepositoryInterface) -> None:
        """Inject the repository dependency.

        Args:
            repository (AccountRepositoryInterface): A concrete
                implementation of the account storage interface.
        """
        self._repository: AccountRepositoryInterface = repository

    # ------------------------------------------------------------------
    # Authentication
    # ------------------------------------------------------------------

    def login(self, username: str, password: str) -> str:
        """Authenticate a user by username and password.

        Args:
            username (str): The account holder's username.
            password (str): The password to verify.

        Returns:
            str: "Login success" or "Login failed".
        """
        pass

    # ------------------------------------------------------------------
    # Financial operations (stubs)
    # ------------------------------------------------------------------

    def deposit(self, username: str, amount: float) -> str:
        """Add funds to an account and record the transaction.

        Args:
            username (str): Target account username.
            amount (float): Positive amount to deposit.

        Returns:
            str: Result message.
        """
        pass

    def withdraw(self, username: str, amount: float) -> str:
        """Deduct funds from an account if balance is sufficient.

        Args:
            username (str): Target account username.
            amount (float): Positive amount to withdraw.

        Returns:
            str: Result message.
        """
        pass

    def transfer(self, username: str, target_username: str, amount: float) -> str:
        """Move funds from one account to another.

        Args:
            username (str): Source account username.
            target_username (str): Destination account username.
            amount (float): Positive amount to transfer.

        Returns:
            str: Result message.
        """
        pass