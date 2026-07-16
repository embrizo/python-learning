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
