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
