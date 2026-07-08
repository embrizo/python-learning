# Month 1, Day 4: Modules & JSON

Welcome to the documentation for Month 1, Day 4 of the AI Engineer Bootcamp. This day focuses on python packages, custom modules, absolute path references, import behaviors, and JSON data persistence.

---

## 📂 Project Structure

The codebase is organized into utility modules and a cohesive modular sub-package representing an **ATM CLI System**.

```text
Day4/
│
├── main.py                     # Entry point for testing basic utility modules
├── student.json                # JSON data for student metadata
├── temperature.py              # Temperature conversion module
│
├── utils/                      # Utilities Package
│   ├── __init__.py             # Package initializer
│   ├── converter.py            # Currency converter module (USD <-> THB)
│   ├── finance.py              # ROI & profit calculation module
│   └── math_untils.py          # Math helper module (addition)
│
└── atm/                        # ATM Package
    ├── __init__.py             # Package initializer
    ├── main.py                 # ATM program entry point & main loop
    ├── auth.py                 # User authentication (login validation)
    ├── banking.py              # Financial transaction logic (deposit, withdraw, transfer)
    ├── storage.py              # State management & JSON persistence
    ├── ui.py                   # User interface menus & screen displays
    └── account.json            # Database storing encrypted/raw user accounts
```

---

## 🔧 Module Details & Code Source

### 1. Root & General Utilities

#### 📝 [main.py](file:///C:/Users/Pattapon/Documents/antigravity/intelligent-newton/python-learning/Month1/Day4/main.py)
Loads package modules (`temperature`, `utils.finance`, `utils.converter`, `utils.math_untils`) and reads the local `student.json` file using an absolute path to output contents.
```python
import temperature as temp 
import utils.finance as finance
import utils.converter as converter
import utils.math_untils as math_untils
import os
import json

# Get the directory of the current script to save the json file in the same folder
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, "student.json")

with open(DATA_FILE) as file:  
    student = json.load(file)
    
print(student)   
```

#### 📝 [student.json](file:///C:/Users/Pattapon/Documents/antigravity/intelligent-newton/python-learning/Month1/Day4/student.json)
A simple JSON structure holding mock student details:
```json
{
    "name": "New",
    "major": "Mechatronics",
    "gpa": 3.45
}
```

#### 📝 [temperature.py](file:///C:/Users/Pattapon/Documents/antigravity/intelligent-newton/python-learning/Month1/Day4/temperature.py)
Implements temperature conversion functions Celsius <-> Fahrenheit:
```python
def celsius_to_fahrenheit():
    c = int(input("Input Celsius = "))
    f = 9/5*c + 32
    return f


def fahrenheit_to_celsius():
    f = int(input("Input Fahrenheit = "))
    c = (f - 32) * 5/9
    return c
```

---

### 2. Utils Package (`utils/`)

#### 📝 [utils/converter.py](file:///C:/Users/Pattapon/Documents/antigravity/intelligent-newton/python-learning/Month1/Day4/utils/converter.py)
Currency conversion between THB and USD based on a fixed exchange rate of `36.22`.
```python
def usd_to_thb():
    usd = float(input("Input USD = "))
    thb = usd * 36.22
    return thb

def thb_to_usd():
    thb = float(input("Input THB = "))
    usd = thb / 36.22
    return usd
```

#### 📝 [utils/finance.py](file:///C:/Users/Pattapon/Documents/antigravity/intelligent-newton/python-learning/Month1/Day4/utils/finance.py)
Performs financial assessments (Simple Interest & Profit/Loss):
```python
def calculate_roi():
    p = input("Enter the principal amount: ")
    r = input("Enter the rate of interest: ")
    t = input("Enter the time in years: ")
    return (int(p)*int(r)*int(t))/100

def calculate_profit():
    invest = input(f"Enter amount Invest = ")
    now = input(f"Enter amount now price = ")
    return (int(now)-int(invest))
```

#### 📝 [utils/math_untils.py](file:///C:/Users/Pattapon/Documents/antigravity/intelligent-newton/python-learning/Month1/Day4/utils/math_untils.py)
Implements a simple interactive number addition function:
```python
def add():
    a = int(input(f"Input a number = "))
    b = int(input(f"Input a number = "))
    c = a + b
    return c
```

---

### 3. ATM CLI Package (`atm/`)

This package is a refactored, modularized version of the Day 2 ATM project, introducing filesystem state persistence.

#### 📝 [atm/main.py](file:///C:/Users/Pattapon/Documents/antigravity/intelligent-newton/python-learning/Month1/Day4/atm/main.py)
Main application loop. Validates login status and routes user menu choices to the relevant banking actions.
```python
from auth import login
from ui import show_menu
from ui import check_balance
from ui import show_history
from banking import deposit, withdraw, transfer
from storage import changepass


def main():
    if login():
        while True:
            show_menu()
            choice = input("Enter your choice: ")
            if choice == "1":
                deposit()
            elif choice == "2":
                withdraw()
            elif choice == "3":
                check_balance()
            elif choice == "4":
                show_history()
            elif choice == "5":
                transfer()
            elif choice == "6":
                changepass()
            elif choice == "7":
                break



main()
```

#### 📝 [atm/auth.py](file:///C:/Users/Pattapon/Documents/antigravity/intelligent-newton/python-learning/Month1/Day4/atm/auth.py)
Prompts for login credentials and verifies them against the accounts stored in memory. Sets the active user context upon success.
```python
import storage

def login():
    storage.load_accounts()
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    
    for account in storage.accounts:
        if username == account["username"] and password == account["password"]:
            storage.set_current_account(account)
            print("Login successful")
            return True
            
    print("Login failed")
    return False
```

#### 📝 [atm/banking.py](file:///C:/Users/Pattapon/Documents/antigravity/intelligent-newton/python-learning/Month1/Day4/atm/banking.py)
Processes financial business rules (Deposit, Withdraw, and Transfer):
```python
import storage

def deposit():
    account = storage.get_current_account()
    if not account:
        print("No user logged in.")
        return
    amount = float(input("Enter amount to deposit: "))
    account["balance"] += amount
    account["history"].append(amount)
    storage.save_accounts()
    print("Deposit successful")

def withdraw():
    account = storage.get_current_account()
    if not account:
        print("No user logged in.")
        return
    amount = float(input("Enter amount to withdraw: "))
    if amount > account["balance"]:
        print("Insufficient balance!")
    else:
        account["balance"] -= amount
        account["history"].append(-amount)
        storage.save_accounts()
        print("Withdraw successful")

def transfer():
    account = storage.get_current_account()
    if not account:
        print("No user logged in.")
        return
    
    target_username = input("Enter username of the person you want to transfer to: ")
    amount = float(input("Enter amount to transfer: "))
    
    if amount > account["balance"]:
        print("Insufficient balance!")
        return
        
    # Find the target account
    target_account = None
    for acc in storage.accounts:
        if acc["username"] == target_username:
            target_account = acc
            break
            
    if target_account is None:
        print(f"Target account '{target_username}' not found!")
        return
        
    # Perform transfer
    account["balance"] -= amount
    account["history"].append(-amount)
    
    target_account["balance"] += amount
    target_account["history"].append(amount)
    
    storage.save_accounts()
    print(f"Transfer to {target_username}'s account successful")
```

#### 📝 [atm/storage.py](file:///C:/Users/Pattapon/Documents/antigravity/intelligent-newton/python-learning/Month1/Day4/atm/storage.py)
Handles loading/saving of account information to `account.json` using absolute directories. Manages global states for `accounts` and `current_account`, including password updates (`changepass()`).
```python
import os
import json

# Get the directory of the current script to save the json file in the same folder
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, "account.json")

# Globally accessible variables in this module
accounts = []
current_account = None

def load_accounts():
    global accounts
    with open(DATA_FILE) as file:  
        accounts = json.load(file)
    return accounts

def save_accounts():
    with open(DATA_FILE, "w") as file:  
        json.dump(accounts, file, indent=4)

def set_current_account(account):
    global current_account
    current_account = account

def get_current_account():
    return current_account

def changepass():
    global current_account
    if current_account is None:
        print("No user logged in.")
        return
    print(f"Your old password is {current_account['password']}")
    password = input("Enter your new password: ")
    current_account["password"] = password
    save_accounts()
    print("Change password successful")

# Load accounts initially
accounts = load_accounts()
```

#### 📝 [atm/ui.py](file:///C:/Users/Pattapon/Documents/antigravity/intelligent-newton/python-learning/Month1/Day4/atm/ui.py)
Standard CLI output renderer for menus, current balances, and historic transactions.
```python
import storage

def show_menu():
    print("1. Deposit")
    print("2. Withdraw")
    print("3. Show Balance")
    print("4. Show History")
    print("5. Transfer")
    print("6. Change Password")
    print("7. Exit")

def check_balance():
    account = storage.get_current_account()
    if account:
        print(f"Balance: {account['balance']}")
    else:
        print("No user logged in.")

def show_history():
    account = storage.get_current_account()
    if account:
        print(f"History: {account['history']}")
    else:
        print("No user logged in.")
```

#### 📝 [atm/account.json](file:///C:/Users/Pattapon/Documents/antigravity/intelligent-newton/python-learning/Month1/Day4/atm/account.json)
Local database containing stored JSON lists representing user profiles, password, balance, and transaction history.
```json
[
    {
        "username": "Pattapon",
        "password": "5555",
        "balance": 20000.0,
        "history": [
            10000.0
        ]
    },
    {
        "username": "admin",
        "password": "1111",
        "balance": 10000,
        "history": []
    }
]
```

---

## 🔍 Key Learning Outcomes

1. **Package Initialization**: Utilizing `__init__.py` files to define package scopes (`utils`, `atm`).
2. **JSON Serialization**: Writing with `json.dump()` and parsing with `json.load()`.
3. **Module Resolution**: Handling path structures dynamically with `os.path.dirname(os.path.abspath(__file__))`.
4. **State Persistence**: Modifying mutable memory representations (dictionaries) and writing them back to disk.
