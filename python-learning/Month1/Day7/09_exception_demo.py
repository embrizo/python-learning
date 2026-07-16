import json
import os

class InsufficientBalanceError(Exception):
    """Raised when account balance is insufficient."""

balance = 50
try:
    amount = float(input("Amount: "))
    if amount > balance:
        raise InsufficientBalanceError(amount)
except ValueError:
    print("Invalid amount.")
except InsufficientBalanceError as e:
    print(f"Error WTF!! Hell: {e}")



try:
    ...
except ValueError:
    ...
except FileNotFoundError:
    ...
except PermissionError:
    ...

def load(filename = "10_account.json"):
    if not os.path.isabs(filename):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(script_dir, filename)
        
    if not os.path.exists(filename):
        raise FileNotFoundError
    with open(filename, encoding="utf-8") as file:
        return json.load(file)

    
try:
    data = load()
    print("Loaded data:", data)
except FileNotFoundError:
    print("File not found.")
finally:
    print("Completed exception handling demo.")



