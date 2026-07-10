class Animal:
    def speak(self):
        print("...")

class Dog(Animal):
    def bark(self):
        print("Woof")

dog = Dog()
dog.speak()
dog.bark()

class User:
    def __init__(self,username:str,password:str):
        self.username = username
        self.__password = password

    @property
    def password(self):
        return self.__password

    def update_password(self, new_password: str) -> None:
        self.__password = new_password #กำหนด Instance Variable ผ่าน self
        
class Accout(User):
    def __init__(self,username:str,password:str,balance:float)->None:
        self.balance = balance
        self.history = []
        super().__init__(username,password)


acc1 = Accout("bank",1234,1000.0)
print(acc1.username)
print(acc1.password)
print(acc1.balance)
new_pass = 1111
acc1.update_password(new_pass)
print(acc1.password)

