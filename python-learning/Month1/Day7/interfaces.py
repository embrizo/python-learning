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
