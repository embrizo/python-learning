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

## 🔧 Module Details

### 1. Root & General Utilities

* **[main.py](file:///C:/Users/Pattapon/Documents/antigravity/intelligent-newton/python-learning/Month1/Day4/main.py)**: Loads package modules (`temperature`, `utils.finance`, `utils.converter`, `utils.math_untils`) and reads the local `student.json` file using an absolute path to output contents.
* **[student.json](file:///C:/Users/Pattapon/Documents/antigravity/intelligent-newton/python-learning/Month1/Day4/student.json)**: A simple JSON structure holding mock student details:
  ```json
  {
      "name": "New",
      "major": "Mechatronics",
      "gpa": 3.45
  }
  ```
* **[temperature.py](file:///C:/Users/Pattapon/Documents/antigravity/intelligent-newton/python-learning/Month1/Day4/temperature.py)**: Implements temperature conversion functions:
  * `celsius_to_fahrenheit()`
  * `fahrenheit_to_celsius()`

### 2. Utils Package (`utils/`)

* **[converter.py](file:///C:/Users/Pattapon/Documents/antigravity/intelligent-newton/python-learning/Month1/Day4/utils/converter.py)**: Currency conversion between THB and USD based on a fixed rate of `36.22`.
* **[finance.py](file:///C:/Users/Pattapon/Documents/antigravity/intelligent-newton/python-learning/Month1/Day4/utils/finance.py)**: Performs financial assessments:
  * ROI / Simple interest calculator (`calculate_roi`)
  * profit/loss calculator (`calculate_profit`)
* **[math_untils.py](file:///C:/Users/Pattapon/Documents/antigravity/intelligent-newton/python-learning/Month1/Day4/utils/math_untils.py)**: Implements a simple interactive number addition function (`add`).

### 3. ATM CLI Package (`atm/`)

This package is a refactored, modularized version of the Day 2 ATM project, introducing filesystem state persistence.

* **[main.py](file:///C:/Users/Pattapon/Documents/antigravity/intelligent-newton/python-learning/Month1/Day4/atm/main.py)**: Main application loop. Validates login status and routes user menu choices to the relevant banking actions.
* **[auth.py](file:///C:/Users/Pattapon/Documents/antigravity/intelligent-newton/python-learning/Month1/Day4/atm/auth.py)**: Prompts for login credentials and verifies them against the accounts stored in memory. Sets the active user context upon success.
* **[banking.py](file:///C:/Users/Pattapon/Documents/antigravity/intelligent-newton/python-learning/Month1/Day4/atm/banking.py)**: Processes financial business rules:
  * `deposit()`: Increases user balance and records positive transactions.
  * `withdraw()`: Checks current balance and processes withdrawals.
  * `transfer()`: Resolves target account name, validates funds, and handles inter-account transfers.
* **[storage.py](file:///C:/Users/Pattapon/Documents/antigravity/intelligent-newton/python-learning/Month1/Day4/atm/storage.py)**: Handles loading/saving of account information to `account.json` using absolute directories. Manages global states for `accounts` and `current_account`, including password updates (`changepass()`).
* **[ui.py](file:///C:/Users/Pattapon/Documents/antigravity/intelligent-newton/python-learning/Month1/Day4/atm/ui.py)**: Standard CLI output renderer for menus, current balances, and historic transactions.
* **[account.json](file:///C:/Users/Pattapon/Documents/antigravity/intelligent-newton/python-learning/Month1/Day4/atm/account.json)**: Local database containing stored JSON lists representing user profiles, password, balance, and transaction history.

---

## 🔍 Key Learning Outcomes

1. **Package Initilization**: Utilizing `__init__.py` files to define package scopes (`utils`, `atm`).
2. **JSON Serialization**: Writing with `json.dump()` and parsing with `json.load()`.
3. **Module Resolution**: Handling path structures dynamically with `os.path.dirname(os.path.abspath(__file__))`.
4. **State Persistence**: Modifying mutable memory representations (dictionaries) and writing them back to disk.
