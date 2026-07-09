# Month 1 — Day 5: Object-Oriented Programming (OOP)

## 🎯 Learning Objectives

เมื่อจบ Day 5 คุณจะสามารถ:
* เข้าใจแนวคิดและโครงสร้างของ **Object-Oriented Programming (OOP)** ในภาษา Python
* สร้างและเรียกใช้งาน **Classes** และ **Objects** ได้อย่างถูกต้อง
* กำหนด **Constructor (`__init__`)** และสร้าง **Methods** ภายใน Class
* ประยุกต์ใช้ **Encapsulation** โดยการสร้าง Private Attributes (`_` และ `__`) และควบคุมผ่าน `@property` (Getter/Setter)
* เปรียบเทียบความแตกต่างระหว่าง OOP ของ Python กับภาษา C# ที่คุ้นเคย
* **Refactor ATM CLI** จากแบบโมดูลทั่วไป (Function-based) ไปเป็นโครงสร้างแบบ OOP (Class-based) เพื่อกำจัด Global Variables และเพิ่มความมั่นคงของข้อมูล

---

## 💡 ทำไมต้องเรียน OOP?

ใน Day 4 ที่ผ่านมา คุณได้แยก ATM ออกเป็นโมดูลต่าง ๆ (`auth.py`, `banking.py`, `storage.py`, `ui.py`)
แต่จุดที่ยังขาดความสมบูรณ์และเป็นความเสี่ยงทางด้านซอฟต์แวร์ก็คือ **การใช้ Global State / Global Variables**
```python
# storage.py (Day 4)
accounts = []
current_account = None
```
การเก็บข้อมูลบัญชีแบบนี้มีข้อเสียร้ายแรง:
1. **Thread-Safety / Concurrency**: หากมีผู้ใช้อื่นเข้ามาพร้อมกัน ตัวแปร `current_account` จะถูกเขียนทับ
2. **Encapsulation**: ทุกฟังก์ชันภายนอกสามารถเข้าไปแก้ไขค่าในดิกชันนารี `current_account` ตรง ๆ ได้ โดยไม่มีการตรวจสอบข้อมูลนำเข้า (Input Validation) เช่น การถอนเงินเป็นค่าลบ

การนำ **OOP** เข้ามาใช้ จะทำการห่อหุ้ม (Encapsulate) ข้อมูลของบัญชีผู้ใช้และพฤติกรรม (การฝาก, ถอน, โอน) ไว้ในออบเจกต์เดียวกัน ซึ่งเรียกว่า **`Account` Class**

---

## 📚 Part 1 — Class & Object (ทฤษฎีและการสร้างคลาส)

**Class** เปรียบเสมือนแบบแปลนบ้าน (Blueprint) และ **Object** เปรียบเสมือนบ้านจริง ๆ ที่สร้างขึ้นมาจากแบบแปลนนั้น

### ⚡ เปรียบเทียบ Python VS C#
* ใน **C#**: ทุกอย่างถูกผูกมัดด้วย Class ตั้งแต่ต้น และจำเป็นต้องระบุ Data Type เสมอ
* ใน **Python**: คลาสมีความยืดหยุ่นสูง (Dynamic) และตัวแปรสมาชิกไม่ต้องระบุก็ได้ แต่เพื่อความเป็นโปรดักชัน เราจะใช้ **Type Hints** ช่วยในการกำหนดประเภทข้อมูล

### ตัวอย่างการสร้าง Class & Object พื้นฐาน
```python
# model_info.py

class AIModel:
    pass  # คลาสว่างเปล่า

# การสร้าง Object (Instantiating)
resnet = AIModel()
bert = AIModel()
```

### 📝 Exercise 1
สร้างไฟล์ `ai_model.py` ประกาศคลาส `AIModel` จากนั้นลองสร้างออบเจกต์ 2 ตัว ชื่อ `gpt4` และ `claude`

---

## 📚 Part 2 — Constructors & Methods (ตัวสร้างและพฤติกรรม)

* **Constructor (`__init__`)**: เป็นเมธอดพิเศษที่จะทำงานโดยอัตโนมัติเมื่อมีการสร้างออบเจกต์ขึ้นมา ทำหน้าที่ตั้งค่าเริ่มต้นให้กับข้อมูล (Attributes) ของออบเจกต์นั้น ๆ
* **`self`**: แทนตัวแปรของออบเจกต์ปัจจุบัน (ทำหน้าที่เหมือน `this` ในภาษา C#) เมธอดทุกตัวในคลาส Python ต้องรับ `self` เป็นพารามิเตอร์ตัวแรกเสมอ

### ตัวอย่างการเขียน Constructor & Method
```python
class AIModel:
    def __init__(self, name: str, framework: str):
        self.name: str = name               # Instance Variable
        self.framework: str = framework     # Instance Variable

    def display_info(self) -> None:
        """พิมพ์รายละเอียดของรุ่นโมเดลปัญญาประดิษฐ์"""
        print(f"Model Name: {self.name} | Framework: {self.framework}")

# สร้างออบเจกต์พร้อมใส่ค่าเริ่มต้น
gpt = AIModel("GPT-4o", "OpenAI API")
gpt.display_info()
```

### 📝 Exercise 2
เพิ่มเมธอด `train(self, epochs: int) -> None` ลงในคลาส `AIModel` จาก Exercise 1 ให้ทำการลูปปริ้น `"Training epoch {i}..."` ตามจำนวนรอบที่ส่งเข้ามา

---

## 📚 Part 3 — Encapsulation & Properties (การปกป้องข้อมูล)

ในภาษา C# คุณมี Access Modifiers เช่น `public`, `private`, `protected` เพื่อควบคุมสิทธิ์การเข้าถึงข้อมูล
แต่ใน Python **ไม่มีระบบตรวจสอบสิทธิ์เข้าถึงที่ระดับ Runtime อย่างเข้มงวด** Python จึงใช้ชื่อเป็นตัวระบุข้อตกลงแทน (Convention):

1. **Public**: `self.accuracy = 0.9` (เข้าถึงและแก้ไขตรง ๆ ได้จากทุกที่)
2. **Protected**: `self._accuracy = 0.9` (มีเครื่องหมายขีดล่างเดียว มีความหมายเชิงสัญลักษณ์ว่า *โปรดอย่าเข้าถึงภายนอกคลาส ยกเว้นใน Subclass*)
3. **Private (Name Mangling)**: `self.__accuracy = 0.9` (มีเครื่องหมายขีดล่างสองตัว Python จะทำการแปลงชื่อตัวแปรนี้เป็น `_ClassName__accuracy` เพื่อป้องกันการเข้าถึงตรง ๆ จากภายนอก)

### การควบคุมผ่าน Property (Getter & Setter)
ในการพัฒนาแอปพลิเคชันระดับองค์กร เราจะใช้ `@property` decorator ในการหุ้ม Private Variable เพื่อให้ตรวจสอบความถูกต้อง (Validation) ก่อนบันทึกค่าลงไปได้

```python
class AIModel:
    def __init__(self, name: str):
        self.name: str = name
        self.__accuracy: float = 0.0  # Private variable

    @property
    def accuracy(self) -> float:
        """Getter: ดึงค่า Accuracy ออกมาแสดงผล"""
        return self.__accuracy

    @accuracy.setter
    def accuracy(self, value: float) -> None:
        """Setter: ตรวจสอบความถูกต้องก่อนเขียนทับข้อมูล"""
        if not (0.0 <= value <= 1.0):
            raise ValueError("Accuracy must be between 0.0 and 1.0")
        self.__accuracy = value

# การใช้งาน
model = AIModel("ResNet")
model.accuracy = 0.95  # เรียกใช้งาน Setter ทำงานเบื้องหลัง
print(model.accuracy)   # เรียกใช้งาน Getter -> 0.95
# model.accuracy = 1.5  # เกิดข้อผิดพลาด ValueError!
```

### 📝 Exercise 3
นำคลาส `AIModel` มาทำการครอบตัวแปร `__learning_rate` ด้วย `@property` และ `@learning_rate.setter` โดยมีเงื่อนไขว่าค่า Learning Rate จะต้องมีค่า **มากกว่า 0 เสมอ** ถ้าไม่ผ่านให้แจ้งข้อผิดพลาด

---

## 🚀 Main Project — Refactoring ATM CLI to OOP

เป้าหมายสูงสุดของวันนี้คือการย้ายข้อมูลสถานะของบัญชีธนาคาร จากข้อมูลดิบใน Dictionary ย้ายมาห่อหุ้มใน **`Account` Class** เพื่อความมั่นคงปลอดภัยและความเป็นโมดูลที่ดีขึ้น

### โครงสร้างของไฟล์ใหม่ (Day 5)
```text
Day5/
└── atm/
    ├── __init__.py
    ├── main.py
    ├── account.py        # [NEW] เก็บ Account Class
    ├── auth.py
    ├── banking.py
    ├── storage.py
    ├── ui.py
    └── account.json
```

### แนวทางขั้นตอนการ Refactor

#### 1. ออกแบบไฟล์ `account.py`
สร้างคลาส `Account` สำหรับจัดการบัญชีเดี่ยว:
```python
from typing import List

class Account:
    def __init__(self, username: str, password: str, balance: float, history: List[float]):
        self.username: str = username
        self.__password: str = password  # Private
        self.balance: float = balance
        self.history: List[float] = history

    def verify_password(self, password: str) -> bool:
        """ตรวจสอบความถูกต้องของรหัสผ่าน"""
        return self.__password == password

    def change_password(self, new_password: str) -> None:
        """เปลี่ยนรหัสผ่าน"""
        self.__password = new_password

    def to_dict(self) -> dict:
        """แปลงออบเจกต์กลับเป็น Dictionary สำหรับเขียนลง JSON"""
        return {
            "username": self.username,
            "password": self.__password,
            "balance": self.balance,
            "history": self.history
        }
```

#### 2. แก้ไขไฟล์ `storage.py`
ใน `storage.py` ตัวแปร `accounts` จะเก็บรายการออบเจกต์ `Account` แทนดิคชันนารีดิบ:
```python
import os
import json
from typing import List
from account import Account  # นำเข้าคลาส

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, "account.json")

accounts: List[Account] = []
current_account: Account = None  # จะมีชนิดข้อมูลเป็น Account หรือ None

def load_accounts() -> List[Account]:
    global accounts
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as file:
        raw_data = json.load(file)
        # ทำการ Mapping จาก Dictionary ไปเป็น Object Account
        accounts = [
            Account(
                username=item["username"],
                password=item["password"],
                balance=item["balance"],
                history=item["history"]
            )
            for item in raw_data
        ]
    return accounts

def save_accounts() -> None:
    # แปลง Object กลับไปเป็น JSON serializable dict
    with open(DATA_FILE, "w") as file:
        json_data = [acc.to_dict() for acc in accounts]
        json.dump(json_data, file, indent=4)
```

#### 3. แก้ไขโมดูลอื่น ๆ (`banking.py`, `auth.py`, `ui.py`)
ทำการแก้ไขจุดต่าง ๆ ที่เคยดึงข้อมูลผ่าน Key ของ Dictionary มาเป็นการเรียกใช้งานแอตทริบิวต์และเมธอดของ Class โดยตรง:
* *ตัวอย่าง*: เปลี่ยนจาก `account["balance"] -= amount` ไปเป็น `account.balance -= amount`
* *ตัวอย่าง*: เปลี่ยนจาก `password == account["password"]` ไปเป็น `account.verify_password(password)`

---

## 🏆 Senior Engineer Challenge (ATM v4.0 OOP)

ยกระดับโครงสร้าง ATM ให้เป็นระบบ OOP สมบูรณ์แบบโดยปฏิบัติตามกฎนี้:
1. **Encapsulate Balance**: ปกป้องแอตทริบิวต์ยอดเงินคงเหลือในบัญชี (`__balance`) โดยใช้ `@property`
   * การเพิ่ม/ลดเงิน ต้องใช้เมธอดเฉพาะ เช่น `deposit(amount)` หรือ `withdraw(amount)` เท่านั้น **ห้ามเขียนทับยอดเงินตรง ๆ จากภายนอกคลาส**
   * ตรวจสอบว่า ยอดเงินฝากหรือยอดถอนต้องเป็น **จำนวนบวกมากกว่าศูนย์เสมอ**
2. **Type Hints & Docstrings**: เพิ่มคำอธิบายด้วย Docstrings สไตล์ Google และระบุประเภทข้อมูลสำหรับทุกตัวแปรและฟังก์ชัน
3. **No Global Accounts Reference**: จัดระเบียบ `storage.py` หรือย้ายหน้าที่การจัดการสถานะเซสชันไปเป็น `ATMSession` Class

---

## 💬 Interview Questions

### Q1: `self` ใน Python ทำหน้าที่อะไร และต่างจาก `this` ใน C# อย่างไร?
* **คำตอบ**: `self` ทำหน้าที่อ้างอิงถึงตัวแปรหรือตัวตนของออบเจกต์ (Instance) นั้น ๆ ที่กำลังทำงานอยู่ สำหรับ `this` ใน C# เป็นตัวแปรลับ (Implicit) ที่เรียกใช้งานได้ทันทีภายในคลาสโดยไม่ต้องผ่านอาร์กิวเมนต์ แต่ใน Python จำเป็นต้องส่ง `self` เป็นพารามิเตอร์ตัวแรกในเมธอดเสมออย่างเปิดเผย (Explicit)

### Q2: Name Mangling (double underscore `__`) ใน Python คืออะไร และทำงานอย่างไร?
* **คำตอบ**: เมื่องใส่เครื่องหมาย `__` หน้าตัวแปรในคลาส Python จะทำการเปลี่ยนชื่อตัวแปรนั้นเบื้องหลังเป็น `_ClassName__variableName` อัตโนมัติ เพื่อป้องกันไม่ให้ภายนอกเรียกใช้งานทับหรือแก้ไขตัวแปรได้โดยง่าย แต่ไม่ได้เป็นการปิดกั้นอย่างสมบูรณ์แบบ (ต่างจาก private ใน C# ที่มีกลไกทางฝั่งคอมไพเลอร์เป็นผู้บล็อคสิทธิ์การเข้าถึงอย่างถาวร)

### Q3: ทำไม Python ถึงไม่มี Access Modifiers เช่น public, private, protected เหมือน C#?
* **คำตอบ**: เนื่องจากแนวคิดการออกแบบของ Python ยึดหลักการที่เรียกว่า "We are all consenting adults here" (ทุกคนถือว่าบรรลุนิติภาวะแล้วและรู้ว่ากำลังทำอะไรอยู่) โดยให้ความสำคัญกับความสะดวกและรวดเร็วในการพัฒนา จึงใช้เพียงมาตรฐานข้อตกลงในการตั้งชื่อนำหน้า (Prefix) ด้วยขีดล่างแทนการสร้างระบบกลไกควบคุมสิทธิ์ที่ซับซ้อนในระดับ Compiler

### Q4: `@property` ช่วยให้การเขียน Code ดีขึ้นอย่างไร?
* **คำตอบ**: ช่วยให้เราเขียนโค้ดที่สามารถดึงค่าหรือเซ็ตค่าตัวแปรได้สะดวกขึ้นเหมือนการเข้าถึงตัวแปรปกติ (e.g. `model.accuracy = 0.95`) แต่เบื้องหลังยังคงมีความปลอดภัยของข้อมูล (Encapsulation) เพราะสามารถใส่ตรรกะในการตรวจสอบความถูกต้องของข้อมูล (Validation) และการจัดรูปแบบก่อนประมวลผลได้

---

## 🚀 Git Workflow สำหรับส่งงาน
1. สลับมาที่กิ่งสำหรับเริ่มทำงาน: `git checkout feature/day05-oop-atm`
2. ทำภารกิจการ Refactor และสร้างคลาส
3. รันและตรวจสอบโปรแกรม
4. ตรวจสอบการเพิ่มไฟล์และทำการ Commit:
   ```bash
   git add .
   git commit -m "feat: refactor ATM to complete OOP with Account class"
   ```
