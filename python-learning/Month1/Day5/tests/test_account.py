"""
class Account:
    
    def __init__(self, username):
        self.username = username
        self.balance = 10000

    def deposit(self, amount):
        self.balance += amount

    def say_hello(self):
        print(f"Hello {self.username}")




acc = Account("New")
acc.deposit(2000)

class Dog:
    def __init__(self, name):
        self.name = name

dog1 = Dog("New")
dog2 = Dog("John")

print(dog1.name)
print(dog2.name)
print(acc.balance)
acc.say_hello()
print(acc.balance)
"""

class Student:
    def __init__(self, name, score):
        self.name = name
        self.score = score

    def add_score(self, score):
        self.score += score

    def show(self):
        print(f"Name: {self.name}, Score: {self.score}")


s1 = Student("New", 100)
s2 = Student("John", 80)

s1.add_score(-5)
s2.add_score(30)

s1.show()
s2.show()

class car:  
    def __init__(self, brand, speed):
        self.brand = brand
        self.speed = speed
    def accelerate(self):
        self.speed += 10

    def brake(self):
        self.speed -= 10

    def show(self):
        print(f"Brand: {self.brand}, Speed: {self.speed}")


c1 = car("Toyota", 180)
c2 = car("Honda", 200)
c1.brake()
c2.accelerate()
c1.show()
c2.show()

def deposit(self,amount):

    if amount <= 0:
        raise ValueError("Invalid amount")

    self.balance += amount
    