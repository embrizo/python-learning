# Month 1 — Day 5: Object-Oriented Programming (OOP) Summary

สรุปเนื้อหาและการทำ Refactoring ระบบ ATM CLI จาก Functional-based ให้กลายมาเป็น OOP-based ในบทเรียน Day 5

---

## 🎯 แนวคิดหลักของ OOP ที่นำมาใช้ในวันนี้
1. **Class & Object:** การออกแบบพิมพ์เขียว `Account` เพื่อสร้างตัวแทนบัญชีผู้ใช้งาน (Instance) แต่ละบัญชี แทนการเข้าถึงข้อมูลตรงผ่าน Dictionary
2. **Encapsulation (การห่อหุ้มข้อมูล):** ซ่อนตัวแปรสำคัญอย่างยอดคงเหลือ (`__balance`) และรหัสผ่าน (`__password`) โดยจำกัดให้เข้าถึงและแก้ไขผ่านช่องทางที่คลาสกำหนดไว้เท่านั้น
3. **Properties (@property):** ทำหน้าทำเป็นช่องทางให้ภายนอกดึงข้อมูลยอดเงินคงเหลือไปแสดงผลแบบอ่านอย่างเดียว (Read-Only) ป้องกันการนำค่าไปเปลี่ยนหรือเขียนทับตรง ๆ
4. **Data Persistence Integration:** เชื่อมโยง Object-Oriented เข้ากับระบบเก็บข้อมูลแบบ JSON โดยทำการแปลง Object ไปกลับเป็น Dictionary ผ่านเมธอด `to_dict()`

---

## 📁 โครงสร้างโปรเจกต์ Day 5
```text
Day5/
├── to.md              # [NEW] สรุปเนื้อหาและโค้ดของ Day 5 (ไฟล์นี้)
├── main.py            # จุดเริ่มต้นและลูปแสดงหน้าเมนูของโปรแกรม
├── account.py         # คลาส Account (Blueprint)
├── bank.py            # จัดการล็อกอิน หน้าเมนู แสดงยอดเงิน และประวัติธุรกรรม
├── banking.py         # จัดการการทำธุรกรรม (ฝาก ถอน โอน)
├── storage.py         # โหลด/บันทึกไฟล์ JSON และเก็บ Session บัญชี
└── account.json       # ไฟล์บันทึกข้อมูลบัญชีในเครื่อง
```

---

## 💻 Source Code ทั้งหมดใน Day 5

### 1. [account.py](file:///c:/Users/Pattapon/Documents/antigravity/intelligent-newton/python-learning/Month1/Day5/account.py)
```python
from typing import List

class Account:
    """Represents a bank account with basic operations like deposit, withdraw, and transfer."""

    def __init__(self, username: str, password: str, balance: float, history: List[float]):
        """Initialize a new Account instance."""
        self.username: str = username
        self.__password: str = password
        self.__balance: float = balance
        self.history: List[float] = history

    @property
    def balance(self) -> float:
        """Get the current account balance."""
        return self.__balance

    def verify_password(self, password: str) -> bool:
        """Verify if the provided password matches the account password."""
        return self.__password == password

    def change_password(self, new_password: str) -> None:
        """Change the account password."""
        self.__password = new_password

    def deposit(self, amount: float) -> None:
        """Deposit a positive amount into the account."""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.__balance += amount
        self.history.append(amount)

    def withdraw(self, amount: float) -> None:
        """Withdraw a positive amount from the account."""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.__balance:
            raise ValueError("Insufficient balance.")
        self.__balance -= amount
        self.history.append(-amount)

    def transfer(self, target_account: 'Account', amount: float) -> None:
        """Transfer a positive amount to another Account."""
        if amount <= 0:
            raise ValueError("Transfer amount must be positive.")
        if amount > self.__balance:
            raise ValueError("Insufficient balance for transfer.")
        self.withdraw(amount)
        target_account.deposit(amount)

    def print_history(self) -> None:
        """Print the transaction history of this account."""
        if self.history:
            print(f"Transaction History for {self.username}: {self.history}")
        else:
            print(f"No transaction history for {self.username}.")

    def to_dict(self) -> dict:
        """Convert the Account object back to a dictionary for JSON serialization."""
        return {
            "username": self.username,
            "password": self.__password,
            "balance": self.__balance,
            "history": self.history
        }
```

### 2. [storage.py](file:///c:/Users/Pattapon/Documents/antigravity/intelligent-newton/python-learning/Month1/Day5/storage.py)
```python
import os
import json
from typing import List, Optional
from account import Account

# Get the directory of the current script to save the json file in the same folder
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, "account.json")

# Globally accessible variables in this module
accounts: List[Account] = []
current_account: Optional[Account] = None

def load_accounts() -> List[Account]:
    """Load accounts from the JSON file and map them to Account instances."""
    global accounts
    if not os.path.exists(DATA_FILE):
        accounts = []
        return accounts
    
    with open(DATA_FILE, "r") as file:  
        raw_data = json.load(file)
        accounts = []
        for item in raw_data:
            acc = Account(
                username=item["username"],
                password=item["password"],
                balance=float(item["balance"]),
                history=list(item["history"])
            )
            accounts.append(acc)
    return accounts

def save_accounts() -> None:
    """Serialize and save Account objects to the JSON file."""
    with open(DATA_FILE, "w") as file:
        json_data = [acc.to_dict() for acc in accounts]
        json.dump(json_data, file, indent=4)

def set_current_account(account: Account) -> None:
    """Set the currently logged-in account."""
    global current_account
    current_account = account

def get_current_account() -> Optional[Account]:
    """Get the currently logged-in account."""
    global current_account
    return current_account

def changepass() -> None:
    """Prompt the user and change their password using the Account OOP method."""
    global current_account
    if current_account is None:
        print("No user logged in.")
        return
    new_password = input("Enter your new password: ")
    if len(new_password) < 8:
        print(f"Error: Password must be at least 8 characters long")
        return
    else:
        current_account.change_password(new_password)
        save_accounts()
        print("Change password successful")
```

### 3. [bank.py](file:///c:/Users/Pattapon/Documents/antigravity/intelligent-newton/python-learning/Month1/Day5/bank.py)
```python
import storage

def login() -> bool:
    """Prompt the user for credentials and verify them against loaded accounts."""
    storage.load_accounts()
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    for acc in storage.accounts:
        if acc.username == username and acc.verify_password(password):
            storage.set_current_account(acc)
            print("Login successful")
            return True

    print("Login failed")
    return False

def show_menu() -> None:
    """Print the ATM operation menu."""
    print("\n--- ATM Menu ---")
    print("1. Deposit")
    print("2. Withdraw")
    print("3. Show Balance")
    print("4. Show History")
    print("5. Transfer")
    print("6. Change Password")
    print("7. Exit")

def check_balance() -> None:
    """Print the balance of the current logged-in account."""
    account = storage.get_current_account()
    if account:
        print(f"Balance: {account.balance}")
    else:
        print("No user logged in.")

def show_history() -> None:
    """Print the transaction history of the current logged-in account."""
    account = storage.get_current_account()
    if account:
        account.print_history()
    else:
        print("No user logged in.")
```

### 4. [banking.py](file:///c:/Users/Pattapon/Documents/antigravity/intelligent-newton/python-learning/Month1/Day5/banking.py)
```python
import storage

def deposit() -> None:
    """Deposit money into the current logged-in account."""
    account = storage.get_current_account()
    if not account:
        print("No user logged in.")
        return
    try:
        amount = float(input("Enter amount to deposit: "))
        account.deposit(amount)
        storage.save_accounts()
        print("Deposit successful")
    except ValueError as e:
        print(f"Error: {e}")

def withdraw() -> None:
    """Withdraw money from the current logged-in account."""
    account = storage.get_current_account()
    if not account:
        print("No user logged in.")
        return
    try:
        amount = float(input("Enter amount to withdraw: "))
        account.withdraw(amount)
        storage.save_accounts()
        print("Withdraw successful")
    except ValueError as e:
        print(f"Error: {e}")

def transfer() -> None:
    """Transfer money from the current logged-in account to another account."""
    account = storage.get_current_account()
    if not account:
        print("No user logged in.")
        return
    
    target_username = input("Enter username of the person you want to transfer to: ")
    try:
        amount = float(input("Enter amount to transfer: "))
    except ValueError:
        print("Error: Invalid amount format.")
        return
        
    target_account = None
    for acc in storage.accounts:
        if acc.username == target_username:
            target_account = acc
            break
            
    if target_account is None:
        print(f"Target account '{target_username}' not found!")
        return
        
    try:
        account.transfer(target_account, amount)
        storage.save_accounts()
        print(f"Transfer to {target_username}'s account successful")
    except ValueError as e:
        print(f"Error: {e}")
```

### 5. [main.py](file:///c:/Users/Pattapon/Documents/antigravity/intelligent-newton/python-learning/Month1/Day5/main.py)
```python
from bank import login, show_menu, check_balance, show_history
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
                print("Thank you for using the ATM.")
                break

if __name__ == "__main__":
    main()
```
