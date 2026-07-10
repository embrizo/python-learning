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
