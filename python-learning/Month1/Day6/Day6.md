# Day 6: Object-Oriented Programming (OOP) & Clean Architecture

On Day 6, we explore advanced Object-Oriented Programming (OOP) concepts in Python and apply them to build a modular bank application using **Clean Architecture** principles.

---

## 1. Core OOP Concepts & Demos

### A. Inheritance (การสืบทอดคุณสมบัติ)
Inheritance allows a child class to inherit attributes and methods from a parent class, promoting code reuse.
* **File:** [inheritance_demo.py](file:///c:/Users/Pattapon/Documents/antigravity/intelligent-newton/python-learning/Month1/Day6/inheritance_demo.py)

```python
class Animal:
    def speak(self):
        print("...")

class Dog(Animal):
    def bark(self):
        print("Woof")

dog = Dog()
dog.speak()
dog.bark()

class User:
    def __init__(self,username:str,password:str):
        self.username = username
        self.__password = password

    @property
    def password(self):
        return self.__password

    def update_password(self, new_password: str) -> None:
        self.__password = new_password #กำหนด Instance Variable ผ่าน self
        
class Accout(User):
    def __init__(self,username:str,password:str,balance:float)->None:
        self.balance = balance
        self.history = []
        super().__init__(username,password)


acc1 = Accout("bank",1234,1000.0)
print(acc1.username)
print(acc1.password)
print(acc1.balance)
new_pass = 1111
acc1.update_password(new_pass)
print(acc1.password)
```

---

### B. Polymorphism (การพหุสัณฐาน)
Polymorphism allows different classes to implement methods with the same name, enabling uniform interface handling for diverse types.
* **File:** [polymorphism_demo.py](file:///c:/Users/Pattapon/Documents/antigravity/intelligent-newton/python-learning/Month1/Day6/polymorphism_demo.py)

```python
class Cat:

    def speak(self):
        print("Meow")

class Dog:
    def speak(self):
        print("Woof")

animals = [Cat(),Dog()]
for animal in animals:
    animal.speak()


class OpenAIModel:

    def prompt(self,msg:str)->str:
        return f"OpenAI: {msg}"

class GeminiModel:
    def prompt(self,msg:str)->str:
        return f"Gemini: {msg}"

class DeepSeekModel:
    def prompt(self,msg:str)->str:
        return f"DeepSeek: {msg}"


models = [OpenAIModel(),GeminiModel(),DeepSeekModel()]

for model in models:
    print(model.prompt("Hello"))
```

---

### C. Composition (การประกอบวัตถุ)
Composition involves building complex classes by combining other objects rather than relying solely on inheritance ("has-a" relationship instead of "is-a").
* **File:** [composition_demo.py](file:///c:/Users/Pattapon/Documents/antigravity/intelligent-newton/python-learning/Month1/Day6/composition_demo.py)

```python
class Engine:

    def start(self):
        print("Engine Started")

class Car:

    def __init__(self):
        self.engine = Engine()



car = Car() 
car.engine.start()   

class Electic_Car:
    def __init__(self):
        self.engine = Engine()


elec_car = Electic_Car()
elec_car.engine.start()

class Account:
    def __init__(self,username:str,password:str,balance:float)->None:
        self.username = username
        self.__password = password
        self._balance = balance

    def __str__(self)->str:
        return f"Username:{self.username}, Balance:{self._balance}"
    
    @property
    def password(self)->str:
        return self.__password
    
    @password.setter
    def password(self,value:str)->None:
        self.__password = value    

class TransectionHistory:
    def history(self,history:list[float])->list[float]:
        return history

class BankService:
    def __init__(self,account:Account,transaction_history:TransectionHistory):
        self.account = account
        self.transaction_history = transaction_history
    
acc1 = Account("Pattapon","1234",10000.0)

print(acc1)
```

---

### D. Dataclasses (ดาต้าคลาส)
`dataclasses` simplify writing classes that primarily hold data by auto-generating boilerplate methods like `__init__`, `__repr__`, and `__eq__`.
* **File:** [dataclasses_demo.py](file:///c:/Users/Pattapon/Documents/antigravity/intelligent-newton/python-learning/Month1/Day6/dataclasses_demo.py)

```python
from importlib import resources
from abc import ABC, abstractmethod
class storage(ABC):
    @abstractmethod
    def save():
        pass

from dataclasses import dataclass
@dataclass
class User:
    name: str
    age: int

    def save(self):
        print("User saved to storage")

@dataclass
class Prompt:

    system:str

    user:str

    temperature:float        
```

---

## 2. Bank CLI System Design (Clean Architecture)

We designed a fully separated Bank system following **Dependency Inversion Principle (DIP)**:
1. **Domain Layer:** Models and entity structures (`model.py`, `transactions.py`).
2. **Abstractions Layer:** Interface contracts (`interfaces.py`).
3. **Data Access Layer:** Repository implementation (`repository.py`).
4. **Service Layer:** Business operations / Logic (`services.py`).
5. **Presentation Layer:** Command line loop entrypoint (`main.py`).

Here is the source code of the component layers:

### Domain Entities
* **File:** [transactions.py](file:///c:/Users/Pattapon/Documents/antigravity/intelligent-newton/python-learning/Month1/Day6/transactions.py)
```python
from typing import Optional
from dataclasses import dataclass
@dataclass
class Transaction:
    type:str
    amount:float
    timestamp:str
    note: Optional[str] = None

    def __str__(self)->str:
        return f"{self.timestamp} - {self.type} - {self.amount} - {self.note}"
```

* **File:** [model.py](file:///c:/Users/Pattapon/Documents/antigravity/intelligent-newton/python-learning/Month1/Day6/model.py)
```python
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
```

### Abstractions (Contracts)
* **File:** [interfaces.py](file:///c:/Users/Pattapon/Documents/antigravity/intelligent-newton/python-learning/Month1/Day6/interfaces.py)
```python
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Optional


class AccountRepositoryInterface(ABC):
    """Abstract interface (contract) for Account storage operations.

    Any concrete repository (JSON, SQLite, in-memory, etc.) must
    implement all three abstract methods below.
    """

    @abstractmethod
    def save(self, account) -> None:
        """Persist an account to storage.

        Args:
            account (Account): The account object to save.
        """
        pass

    @abstractmethod
    def find_by_username(self, username: str):
        """Retrieve an account by username.

        Args:
            username (str): The unique username to search for.

        Returns:
            Optional[Account]: The matching Account, or None if not found.
        """
        pass

    @abstractmethod
    def load_all(self) -> List:
        """Load every account from storage.

        Returns:
            List[Account]: All stored accounts.
        """
        pass
```

### Data Access Layer (Repository Pattern)
* **File:** [repository.py](file:///c:/Users/Pattapon/Documents/antigravity/intelligent-newton/python-learning/Month1/Day6/repository.py)
```python
from __future__ import annotations
import json
import os
from typing import List, Optional

from interfaces import AccountRepositoryInterface
from model import Account
from transactions import Transaction


class JsonRepository(AccountRepositoryInterface):
    """Concrete repository that persists Account data as JSON.

    Each account is stored in a JSON file at *file_path*.
    The file contains a list of account objects serialised as dicts.

    Args:
        file_path (str): Path to the JSON data file.
    """

    def __init__(self, file_path: str = "account.json") -> None:
        """Initialise with the path to the backing JSON file.

        Args:
            file_path (str): Relative or absolute path to the JSON file.
                             Defaults to "account.json".
        """
        self.file_path: str = file_path

    # ------------------------------------------------------------------
    # AccountRepositoryInterface implementation (stubs)
    # ------------------------------------------------------------------

    def save(self, account: Account) -> None:
        """Serialise and persist *account* to the JSON file.

        Args:
            account (Account): The account to save or update.
        """
        pass

    def find_by_username(self, username: str) -> Optional[Account]:
        """Search the JSON file for an account matching *username*.

        Args:
            username (str): The username to look up.

        Returns:
            Optional[Account]: Matching Account or None.
        """
        pass

    def load_all(self) -> List[Account]:
        """Read the JSON file and deserialise all accounts.

        Returns:
            List[Account]: All accounts found in storage.
        """
        pass

    # ------------------------------------------------------------------
    # Private helpers (stubs)
    # ------------------------------------------------------------------

    def _read_raw(self) -> List[dict]:
        """Read the raw JSON file and return a list of account dicts.

        Returns:
            List[dict]: Raw data from the file, or empty list if missing.
        """
        pass

    def _write_raw(self, data: List[dict]) -> None:
        """Overwrite the JSON file with *data*.

        Args:
            data (List[dict]): Serialised account records to persist.
        """
        pass

    def _account_to_dict(self, account: Account) -> dict:
        """Convert an Account domain object to a plain dict for JSON.

        Args:
            account (Account): The account to serialise.

        Returns:
            dict: JSON-serialisable representation of the account.
        """
        pass

    def _dict_to_account(self, data: dict) -> Account:
        """Reconstruct an Account domain object from a raw dict.

        Args:
            data (dict): Dict loaded from the JSON file.

        Returns:
            Account: The hydrated Account object.
        """
        pass
```

### Business Logic Layer (Service Pattern)
* **File:** [services.py](file:///c:/Users/Pattapon/Documents/antigravity/intelligent-newton/python-learning/Month1/Day6/services.py)
```python
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
```

### Entry Point & Interactive CLI
* **File:** [main.py](file:///c:/Users/Pattapon/Documents/antigravity/intelligent-newton/python-learning/Month1/Day6/main.py)
```python
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
```

---

## 3. Test Suites

### A. Account Tests
* **File:** [tests/test_account.py](file:///c:/Users/Pattapon/Documents/antigravity/intelligent-newton/python-learning/Month1/Day6/tests/test_account.py)

```python
class User:
    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.__password = password
    @property    
    def password(self)->str:
        return self.__password

    @password.setter
    def password(self,value:str)->None:
        self.__password = value    

class Account(User):
    def __init__(self,username:str,password:str,balance:float)->None:
        self.balance = balance
        self.history = []
        super().__init__(username,password)    


acc1 = Account("Pattapon",5555,10000.0)
print(acc1.username)
print(acc1._User__password)
print(acc1.balance)
print(acc1.history)

acc2 = Account("Somsak","1111",20000.0)
print(acc2.username)
print(acc2._User__password)
print(acc2.balance)
print(acc2.history)

acc1.password = "9999"
print(acc1.password)
```

---

### B. Repository Unit Tests
* **File:** [tests/test_repository.py](file:///c:/Users/Pattapon/Documents/antigravity/intelligent-newton/python-learning/Month1/Day6/tests/test_repository.py)

```python
import sys
import os
import unittest
from unittest.mock import MagicMock, patch

# Allow imports from the parent Day6 directory
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from repository import JsonRepository
from model import Account


class TestJsonRepository(unittest.TestCase):
    """Test suite for the JsonRepository data-access layer."""

    def setUp(self) -> None:
        """Initialise repository pointing at a temp test file."""
        self.repo = JsonRepository(file_path="test_data.json")
        self.sample_account = Account(
            username="alice", password="pass123", balance=500.0
        )

    def test_save_creates_or_updates_entry(self) -> None:
        """Saving an account should persist it to the JSON file."""
        pass  # TODO: call save(), then find_by_username() and assert

    def test_find_by_username_returns_account(self) -> None:
        """Should return the correct Account for a known username."""
        pass  # TODO: seed data, call find_by_username(), assert

    def test_find_by_username_returns_none_for_unknown(self) -> None:
        """Should return None when username does not exist."""
        pass  # TODO: call find_by_username("nobody"), assert None

    def test_load_all_returns_list(self) -> None:
        """load_all() should always return a list (empty or populated)."""
        pass  # TODO: call load_all(), assert isinstance(result, list)

    def test_account_serialisation_round_trip(self) -> None:
        """_account_to_dict + _dict_to_account should be lossless."""
        pass  # TODO: serialise then deserialise, compare fields

    def tearDown(self) -> None:
        """Remove temporary test file if it was created."""
        if os.path.exists("test_data.json"):
            os.remove("test_data.json")


if __name__ == "__main__":
    unittest.main()
```
