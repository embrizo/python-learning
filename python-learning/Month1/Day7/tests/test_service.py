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

def test_withdraw_insufficient_balance(bank_service):
    service, _ = bank_service
    service.register("alice", "pass123", 100.0)
    
    with pytest.raises(InsufficientBalanceError) as exc_info:
        service.withdraw("alice", 150.0)
    assert "Insufficient balance" in str(exc_info.value)

def test_withdraw_invalid_amount(bank_service):
    service, _ = bank_service
    service.register("alice", "pass123", 100.0)
    
    with pytest.raises(InvalidAmountError):
        service.withdraw("alice", -5.0)

# --- 5. Transfer tests ---
def test_transfer_success(bank_service):
    service, repo = bank_service
    service.register("alice", "pass123", 100.0)
    service.register("bob", "pass456", 50.0)
    
    service.transfer("alice", "bob", 30.0)
    
    acc_alice = repo.find_by_username("alice")
    acc_bob = repo.find_by_username("bob")
    
    assert acc_alice.balance == 70.0
    assert acc_bob.balance == 80.0
    
    assert len(acc_alice.history) == 1
    assert acc_alice.history[0].type == "Transfer Out"
    assert acc_alice.history[0].amount == 30.0
    assert acc_alice.history[0].note == "Transfer to bob"
    
    assert len(acc_bob.history) == 1
    assert acc_bob.history[0].type == "Transfer In"
    assert acc_bob.history[0].amount == 30.0
    assert acc_bob.history[0].note == "Transfer from alice"

def test_transfer_insufficient_balance(bank_service):
    service, _ = bank_service
    service.register("alice", "pass123", 100.0)
    service.register("bob", "pass456", 50.0)
    
    with pytest.raises(InsufficientBalanceError):
        service.transfer("alice", "bob", 120.0)

def test_transfer_to_self(bank_service):
    service, _ = bank_service
    service.register("alice", "pass123", 100.0)
    
    with pytest.raises(InvalidAmountError) as exc_info:
        service.transfer("alice", "alice", 10.0)
    assert "Cannot transfer to the same account" in str(exc_info.value)

# --- 6. Repository Save & Serialization test ---
def test_repository_save_and_load(bank_service):
    _, repo = bank_service
    acc = Account("charlie", "secret", 200.0)
    repo.save(acc)
    
    # Save a second time (update)
    acc.deposit(100.0)
    repo.save(acc)
    
    loaded = repo.find_by_username("charlie")
    assert loaded is not None
    assert loaded.balance == 300.0
    assert loaded.password == "secret"
