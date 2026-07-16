from __future__ import annotations
from datetime import datetime
from typing import Optional

from interfaces import AccountRepositoryInterface
from model import Account
from transactions import Transaction
from exceptions import (
    AccountNotFoundError,
    AuthenticationError,
    InvalidAmountError,
    InsufficientBalanceError,
    DuplicateAccountError
)
from logger import logger

class BankService:
    """Business-logic layer for banking operations with logging and exceptions."""

    def __init__(self, repository: AccountRepositoryInterface) -> None:
        self._repository: AccountRepositoryInterface = repository

    def register(self, username: str, password: str, initial_balance: float = 0.0) -> Account:
        """Register a new account.

        Raises:
            DuplicateAccountError: If username already exists.
            InvalidAmountError: If initial balance is negative or fields are empty.
        """
        username = username.strip()
        password = password.strip()
        if not username or not password:
            raise InvalidAmountError("Username and password cannot be empty.")
        if initial_balance < 0:
            raise InvalidAmountError("Initial balance cannot be negative.")

        existing = self._repository.find_by_username(username)
        if existing:
            err_msg = f"Registration failed. Username '{username}' already exists."
            logger.error(err_msg)
            raise DuplicateAccountError(err_msg)

        account = Account(username, password, initial_balance)
        self._repository.save(account)
        logger.info(f"User '{username}' registered successfully with balance {initial_balance:.2f}.")
        return account

    def login(self, username: str, password: str) -> Account:
        """Authenticate a user by username and password.

        Raises:
            AccountNotFoundError: If username does not exist.
            AuthenticationError: If credentials do not match.
        """
        username = username.strip()
        account = self._repository.find_by_username(username)
        if not account:
            err_msg = f"Login failed. Account for username '{username}' not found."
            logger.error(err_msg)
            raise AccountNotFoundError(err_msg)

        if account.password != password:
            err_msg = f"Login failed for user '{username}'. Incorrect password."
            logger.error(err_msg)
            raise AuthenticationError(err_msg)

        logger.info(f"User '{username}' logged in successfully.")
        return account

    def deposit(self, username: str, amount: float) -> None:
        """Add funds to an account and record the transaction.

        Raises:
            AccountNotFoundError: If username does not exist.
            InvalidAmountError: If amount is negative or zero.
        """
        username = username.strip()
        try:
            account = self._repository.find_by_username(username)
            if not account:
                raise AccountNotFoundError(f"Account for username '{username}' not found.")

            account.deposit(amount)
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            transaction = Transaction(
                type="Deposit",
                amount=amount,
                timestamp=timestamp,
                note="Deposit to account"
            )
            account.add_transaction(transaction)
            
            self._repository.save(account)
            logger.info(f"Deposit: User '{username}' deposited {amount:.2f} successfully.")
        except Exception as e:
            logger.error(f"Deposit failed for user '{username}': {str(e)}")
            raise

    def withdraw(self, username: str, amount: float) -> None:
        """Deduct funds from an account and record the transaction.

        Raises:
            AccountNotFoundError: If username does not exist.
            InvalidAmountError: If amount is negative or zero.
            InsufficientBalanceError: If amount exceeds balance.
        """
        username = username.strip()
        try:
            account = self._repository.find_by_username(username)
            if not account:
                raise AccountNotFoundError(f"Account for username '{username}' not found.")

            account.withdraw(amount)
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            transaction = Transaction(
                type="Withdrawal",
                amount=amount,
                timestamp=timestamp,
                note="Withdrawal from account"
            )
            account.add_transaction(transaction)
            
            self._repository.save(account)
            logger.info(f"Withdraw: User '{username}' withdrew {amount:.2f} successfully.")
        except Exception as e:
            logger.error(f"Withdrawal failed for user '{username}': {str(e)}")
            raise

    def transfer(self, username: str, target_username: str, amount: float) -> None:
        """Move funds from one account to another.

        Raises:
            AccountNotFoundError: If source or target username does not exist.
            InvalidAmountError: If amount is negative or transfer is to self.
            InsufficientBalanceError: If source account balance is insufficient.
        """
        username = username.strip()
        target_username = target_username.strip()
        try:
            if username == target_username:
                raise InvalidAmountError("Cannot transfer to the same account.")

            source_account = self._repository.find_by_username(username)
            if not source_account:
                raise AccountNotFoundError(f"Source account '{username}' not found.")

            target_account = self._repository.find_by_username(target_username)
            if not target_account:
                raise AccountNotFoundError(f"Recipient account '{target_username}' not found.")

            # Perform operations
            source_account.withdraw(amount)
            target_account.deposit(amount)

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Record source transaction
            source_tx = Transaction(
                type="Transfer Out",
                amount=amount,
                timestamp=timestamp,
                note=f"Transfer to {target_username}"
            )
            source_account.add_transaction(source_tx)

            # Record target transaction
            target_tx = Transaction(
                type="Transfer In",
                amount=amount,
                timestamp=timestamp,
                note=f"Transfer from {username}"
            )
            target_account.add_transaction(target_tx)

            # Save both accounts
            self._repository.save(source_account)
            self._repository.save(target_account)
            logger.info(f"Transfer: {amount:.2f} transferred from '{username}' to '{target_username}' successfully.")
        except Exception as e:
            logger.error(f"Transfer failed from '{username}' to '{target_username}': {str(e)}")
            raise
