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