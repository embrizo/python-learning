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