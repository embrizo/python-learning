# Month 1, Day 7: Exception Handling & Logging

Welcome to the documentation for Month 1, Day 7 of the AI Engineer Bootcamp. This day focuses on implementing production-grade python features: **Robust Exception Handling**, **Structured Logging**, **Context Managers**, **Dependency Inversion with Interfaces**, and **Environment Configuration** (.env parsing).

---

## 📂 Project Structure

The Day 7 project implements a Simple Bank CLI with clear layering, strict input validation, custom error handling, and robust logging to console and file.

```text
Day7/
│
├── .env                        # Local environment configuration
├── .env.example                # Example template for .env configuration
├── config.py                   # Configuration parser supporting dotenv and manual fallback
├── logger.py                   # Application-wide logger setting up console and file handlers
├── exceptions.py               # Application-specific custom exceptions
├── transactions.py             # Data model representing banking transactions
├── model.py                    # Account entity implementing domain business validation logic
├── interfaces.py               # Abstract interface for repository (Dependency Inversion)
├── repository.py               # JSON state persistence implementation
├── services.py                 # Bank business logic orchestrating entities and repository
├── main.py                     # Interactive terminal UI loop
│
├── tests/                      # Testing Package
│   └── test_service.py         # Pytest test cases covering exceptions, transfers, deposits, logins
│
└── bank.log                    # Generated file containing application runtime logs
```

---

## 🔧 Module Details & Code Source

### 1. Configuration & Logging

#### 📝 [.env](file:///C:/Users/Pattapon/Documents/antigravity/intelligent-newton/python-learning/Month1/Day7/.env)
```env
APP_NAME=BankCLI
LOG_LEVEL=INFO
DATA_FILE=account.json
```

#### 📝 [config.py](file:///C:/Users/Pattapon/Documents/antigravity/intelligent-newton/python-learning/Month1/Day7/config.py)
Loads configuration settings from environment variables or parses the local `.env` file manually if `python-dotenv` is not available.
```python
import os

# Get path of .env relative to this file
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")

try:
    from dotenv import load_dotenv
    load_dotenv(env_path)
except ImportError:
    # Fallback to manual parsing if python-dotenv is not installed
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    os.environ[key.strip()] = val.strip()

APP_NAME = os.getenv("APP_NAME", "BankCLI")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
DATA_FILE = os.getenv("DATA_FILE", "account.json")

# Ensure DATA_FILE is resolved relative to the script directory if it's relative
if not os.path.isabs(DATA_FILE):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    DATA_FILE = os.path.join(script_dir, DATA_FILE)
```

#### 📝 [logger.py](file:///C:/Users/Pattapon/Documents/antigravity/intelligent-newton/python-learning/Month1/Day7/logger.py)
Prepares standard logging configuration, formatting log outputs, and directing logs to both the terminal (StreamHandler) and `bank.log` file (FileHandler).
```python
import logging
import os
import config

# Determine log file path in the same directory as this script
script_dir = os.path.dirname(os.path.abspath(__file__))
log_file_path = os.path.join(script_dir, "bank.log")

# Parse log level from config
level = getattr(logging, config.LOG_LEVEL.upper(), logging.INFO)

# Setup logger
logger = logging.getLogger(config.APP_NAME)
logger.setLevel(level)

# Clear existing handlers to avoid duplicates (important for pytest/interactive)
if logger.hasHandlers():
    logger.handlers.clear()

# Create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Console Handler
console_handler = logging.StreamHandler()
console_handler.setLevel(level)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# File Handler
file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
file_handler.setLevel(level)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
```

---

### 2. Exceptions & Domain Layer

#### 📝 [exceptions.py](file:///C:/Users/Pattapon/Documents/antigravity/intelligent-newton/python-learning/Month1/Day7/exceptions.py)
Implements custom exception hierarchy to structure the error domain models explicitly.
```python
class BankError(Exception):
    """Base exception class for all bank-related errors. Requires a message."""
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message: str = message

class InvalidAmountError(BankError):
    """Raised when the transaction amount is negative, zero, or invalid."""
    pass

class AccountNotFoundError(BankError):
    """Raised when an account is not found in the repository."""
    pass

class AuthenticationError(BankError):
    """Raised when credentials/passwords do not match."""
    pass

class InsufficientBalanceError(BankError):
    """Raised when an account does not have enough balance for a transaction."""
    pass

class DuplicateAccountError(BankError):
    """Raised when attempting to register a username that already exists."""
    pass
```

#### 📝 [transactions.py](file:///C:/Users/Pattapon/Documents/antigravity/intelligent-newton/python-learning/Month1/Day7/transactions.py)
```python
from typing import Optional
from dataclasses import dataclass

@dataclass
class Transaction:
    type: str
    amount: float
    timestamp: str
    note: Optional[str] = None

    def __str__(self) -> str:
        return f"{self.timestamp} - {self.type} - {self.amount} - {self.note}"
```

#### 📝 [model.py](file:///C:/Users/Pattapon/Documents/antigravity/intelligent-newton/python-learning/Month1/Day7/model.py)
An Account entity enforcing internal rules (preventing negative deposits, over-drafts, etc.) and raising specific custom exceptions.
```python
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
```

---

### 3. Architecture & Persistence Layers

#### 📝 [interfaces.py](file:///C:/Users/Pattapon/Documents/antigravity/intelligent-newton/python-learning/Month1/Day7/interfaces.py)
Decouples database operations from the business core using the Dependency Inversion Principle.
```python
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from model import Account

class AccountRepositoryInterface(ABC):
    """Abstract interface (contract) for Account storage operations."""

    @abstractmethod
    def save(self, account: Account) -> None:
        """Persist an account to storage."""
        pass

    @abstractmethod
    def find_by_username(self, username: str) -> Optional[Account]:
        """Retrieve an account by username."""
        pass

    @abstractmethod
    def load_all(self) -> List[Account]:
        """Load every account from storage."""
        pass
```

#### 📝 [repository.py](file:///C:/Users/Pattapon/Documents/antigravity/intelligent-newton/python-learning/Month1/Day7/repository.py)
Concrete implementation of the repository contract utilizing JSON persistence and context managers.
```python
import json
import os
from typing import List, Optional

from interfaces import AccountRepositoryInterface
from model import Account
from transactions import Transaction
import config
from logger import logger

class JsonRepository(AccountRepositoryInterface):
    """Concrete repository that persists Account data as JSON using Context Managers."""

    def __init__(self, file_path: str = None) -> None:
        self.file_path: str = file_path if file_path is not None else config.DATA_FILE

    def save(self, account: Account) -> None:
        """Serialise and persist *account* to the JSON file."""
        try:
            accounts = self.load_all()
            # Update existing account or append new one
            found = False
            for i, acc in enumerate(accounts):
                if acc.username == account.username:
                    accounts[i] = account
                    found = True
                    break
            if not found:
                accounts.append(account)
            
            raw_data = [self._account_to_dict(acc) for acc in accounts]
            self._write_raw(raw_data)
            logger.info(f"Successfully saved account: {account.username}")
        except Exception as e:
            logger.error(f"Failed to save account for {account.username}: {str(e)}")
            raise

    def find_by_username(self, username: str) -> Optional[Account]:
        """Search the JSON file for an account matching *username*."""
        try:
            accounts = self.load_all()
            for acc in accounts:
                if acc.username == username:
                    return acc
            return None
        except Exception as e:
            logger.error(f"Failed finding account by username {username}: {str(e)}")
            raise

    def load_all(self) -> List[Account]:
        """Read the JSON file and deserialise all accounts."""
        try:
            raw_data = self._read_raw()
            return [self._dict_to_account(item) for item in raw_data]
        except Exception as e:
            logger.error(f"Failed to load accounts list: {str(e)}")
            raise

    def _read_raw(self) -> List[dict]:
        """Read the raw JSON file using a context manager."""
        if not os.path.exists(self.file_path):
            return []
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                content = file.read().strip()
                if not content:
                    return []
                return json.loads(content)
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error reading database file {self.file_path}: {str(e)}")
            return []
        except IOError as e:
            logger.error(f"I/O error reading database file {self.file_path}: {str(e)}")
            raise

    def _write_raw(self, data: List[dict]) -> None:
        """Overwrite the JSON file with *data* using a context manager."""
        try:
            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)
        except IOError as e:
            logger.error(f"I/O error writing to database file {self.file_path}: {str(e)}")
            raise

    def _account_to_dict(self, account: Account) -> dict:
        """Convert an Account domain object to a plain dict for JSON."""
        history_list = []
        for t in account.history:
            history_list.append({
                "type": t.type,
                "amount": t.amount,
                "timestamp": t.timestamp,
                "note": t.note
            })
        return {
            "username": account.username,
            "password": account.password,
            "balance": account.balance,
            "history": history_list
        }

    def _dict_to_account(self, data: dict) -> Account:
        """Reconstruct an Account domain object from a raw dict."""
        account = Account(
            username=data["username"],
            password=data["password"],
            balance=data.get("balance", 0.0)
        )
        for t_data in data.get("history", []):
            t = Transaction(
                type=t_data["type"],
                amount=t_data["amount"],
                timestamp=t_data["timestamp"],
                note=t_data.get("note")
            )
            account.add_transaction(t)
        return account
```

#### 📝 [services.py](file:///C:/Users/Pattapon/Documents/antigravity/intelligent-newton/python-learning/Month1/Day7/services.py)
Orchestrates domain models and persistence. Contains methods for transfers, withdrawals, deposits, and logins. Directs logging context for successes and failed operations.
```python
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
```

---

### 4. Interactive Console Interface

#### 📝 [main.py](file:///C:/Users/Pattapon/Documents/antigravity/intelligent-newton/python-learning/Month1/Day7/main.py)
```python
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
                # Refresh from repository to have the latest state
                updated = repository.find_by_username(current_user.username)
                if updated:
                    current_user = updated
                print(f"Current Balance: {current_user.balance:.2f} THB")
                
            elif choice == "2":
                try:
                    amount = float(input("Enter deposit amount: ").strip())
                    service.deposit(current_user.username, amount)
                    print(f"Success: Deposited {amount:.2f} THB.")
                except ValueError:
                    print("Error: Invalid number format.")
                except BankError as e:
                    print(f"Error: {e.message}")
                except Exception as e:
                    logger.error(f"Unexpected error during deposit: {str(e)}")
                    print("Error: An unexpected error occurred.")
                    
            elif choice == "3":
                try:
                    amount = float(input("Enter withdrawal amount: ").strip())
                    service.withdraw(current_user.username, amount)
                    print(f"Success: Withdrew {amount:.2f} THB.")
                except ValueError:
                    print("Error: Invalid number format.")
                except BankError as e:
                    print(f"Error: {e.message}")
                except Exception as e:
                    logger.error(f"Unexpected error during withdrawal: {str(e)}")
                    print("Error: An unexpected error occurred.")
                    
            elif choice == "4":
                target = input("Enter recipient username: ").strip()
                try:
                    amount = float(input("Enter transfer amount: ").strip())
                    service.transfer(current_user.username, target, amount)
                    print(f"Success: Transferred {amount:.2f} THB to '{target}'.")
                except ValueError:
                    print("Error: Invalid number format.")
                except BankError as e:
                    print(f"Error: {e.message}")
                except Exception as e:
                    logger.error(f"Unexpected error during transfer: {str(e)}")
                    print("Error: An unexpected error occurred.")
                    
            elif choice == "5":
                updated = repository.find_by_username(current_user.username)
                if updated:
                    current_user = updated
                if not current_user.history:
                    print("No transaction history found.")
                else:
                    print("\n--- Transaction History ---")
                    for tx in current_user.history:
                        print(tx)
                        
            elif choice == "6":
                print(f"Logged out from '{current_user.username}'.")
                current_user = None
            else:
                print("Invalid option, please try again.")

if __name__ == "__main__":
    main()
```

---

### 5. Automated Unit Tests

#### 📝 [tests/test_service.py](file:///C:/Users/Pattapon/Documents/antigravity/intelligent-newton/python-learning/Month1/Day7/tests/test_service.py)
```python
import sys
import os
import pytest

# Add parent directory of tests/ to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from model import Account
from repository import JsonRepository
from services import BankService
from exceptions import (
    AccountNotFoundError,
    AuthenticationError,
    InvalidAmountError,
    InsufficientBalanceError,
    DuplicateAccountError
)

TEST_DB = "test_accounts_db.json"

@pytest.fixture
def clean_db():
    """Fixture to ensure a clean test database file before and after each test."""
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    yield TEST_DB
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

@pytest.fixture
def bank_service(clean_db):
    """Fixture to initialize JsonRepository and BankService with test database."""
    repo = JsonRepository(file_path=clean_db)
    service = BankService(repo)
    return service, repo

# --- 1. Registration & Duplicate tests ---
def test_register_success(bank_service):
    service, repo = bank_service
    acc = service.register("alice", "pass123", 100.0)
    assert acc.username == "alice"
    assert acc.balance == 100.0
    
    # Verify loaded from repo
    loaded = repo.find_by_username("alice")
    assert loaded is not None
    assert loaded.balance == 100.0

def test_register_duplicate(bank_service):
    service, _ = bank_service
    service.register("alice", "pass123", 100.0)
    with pytest.raises(DuplicateAccountError) as exc_info:
        service.register("alice", "newpass", 50.0)
    assert "already exists" in str(exc_info.value)

# --- 2. Login tests ---
def test_login_success(bank_service):
    service, _ = bank_service
    service.register("alice", "pass123", 100.0)
    acc = service.login("alice", "pass123")
    assert acc.username == "alice"
    assert acc.balance == 100.0

def test_login_failed_user_not_found(bank_service):
    service, _ = bank_service
    with pytest.raises(AccountNotFoundError) as exc_info:
        service.login("unknown", "pass123")
    assert "not found" in str(exc_info.value)

def test_login_failed_wrong_password(bank_service):
    service, _ = bank_service
    service.register("alice", "pass123", 100.0)
    with pytest.raises(AuthenticationError) as exc_info:
        service.login("alice", "wrong_pass")
    assert "Incorrect password" in str(exc_info.value)

# --- 3. Deposit tests ---
def test_deposit_success(bank_service):
    service, repo = bank_service
    service.register("alice", "pass123", 100.0)
    service.deposit("alice", 50.0)
    
    acc = repo.find_by_username("alice")
    assert acc.balance == 150.0
    assert len(acc.history) == 1
    assert acc.history[0].type == "Deposit"
    assert acc.history[0].amount == 50.0

def test_deposit_invalid_amount(bank_service):
    service, _ = bank_service
    service.register("alice", "pass123", 100.0)
    
    with pytest.raises(InvalidAmountError):
        service.deposit("alice", -20.0)
        
    with pytest.raises(InvalidAmountError):
        service.deposit("alice", 0.0)

# --- 4. Withdrawal tests ---
def test_withdraw_success(bank_service):
    service, repo = bank_service
    service.register("alice", "pass123", 100.0)
    service.withdraw("alice", 40.0)
    
    acc = repo.find_by_username("alice")
    assert acc.balance == 60.0
    assert len(acc.history) == 1
    assert acc.history[0].type == "Withdrawal"
    assert acc.history[0].amount == 40.0

def test_withdraw_invalid_amount(bank_service):
    service, _ = bank_service
    service.register("alice", "pass123", 100.0)
    
    with pytest.raises(InvalidAmountError):
        service.withdraw("alice", -5.0)

def test_withdraw_insufficient_balance(bank_service):
    service, _ = bank_service
    service.register("alice", "pass123", 100.0)
    
    with pytest.raises(InsufficientBalanceError) as exc_info:
        service.withdraw("alice", 150.0)
    assert "Insufficient balance" in str(exc_info.value)

# --- 5. Transfer tests ---
def test_transfer_success(bank_service):
    service, repo = bank_service
    service.register("alice", "pass123", 100.0)
    service.register("bob", "pass456", 50.0)
    
    service.transfer("alice", "bob", 30.0)
    
    alice = repo.find_by_username("alice")
    bob = repo.find_by_username("bob")
    
    assert alice.balance == 70.0
    assert bob.balance == 80.0
    
    assert alice.history[-1].type == "Transfer Out"
    assert alice.history[-1].amount == 30.0
    assert bob.history[-1].type == "Transfer In"
    assert bob.history[-1].amount == 30.0

def test_transfer_to_self_error(bank_service):
    service, _ = bank_service
    service.register("alice", "pass123", 100.0)
    
    with pytest.raises(InvalidAmountError) as exc_info:
        service.transfer("alice", "alice", 10.0)
    assert "Cannot transfer to the same account" in str(exc_info.value)

def test_transfer_insufficient_balance(bank_service):
    service, _ = bank_service
    service.register("alice", "pass123", 100.0)
    service.register("bob", "pass456", 50.0)
    
    with pytest.raises(InsufficientBalanceError):
        service.transfer("alice", "bob", 200.0)

def test_transfer_recipient_not_found(bank_service):
    service, _ = bank_service
    service.register("alice", "pass123", 100.0)
    
    with pytest.raises(AccountNotFoundError) as exc_info:
        service.transfer("alice", "bob", 10.0)
    assert "Recipient account" in str(exc_info.value)
