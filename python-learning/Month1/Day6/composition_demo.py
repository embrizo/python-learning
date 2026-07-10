class Engine:

    def start(self):
        print("Engine Started")

class Car:

    def __init__(self):
        self.engine = Engine()



car = Car() 
car.engine.start()   

class Electic_Car:
    def __init__(self):
        self.engine = Engine()


elec_car = Electic_Car()
elec_car.engine.start()

class Account:
    def __init__(self,username:str,password:str,balance:float)->None:
        self.username = username
        self.__password = password
        self._balance = balance

    def __str__(self)->str:
        return f"Username:{self.username}, Balance:{self._balance}"
    
    @property
    def password(self)->str:
        return self.__password
    
    @password.setter
    def password(self,value:str)->None:
        self.__password = value    

class TransectionHistory:
    def history(self,history:list[float])->list[float]:
        return history

class BankService:
    def __init__(self,account:Account,transaction_history:TransectionHistory):
        self.account = account
        self.transaction_history = transaction_history
    
acc1 = Account("Pattapon","1234",10000.0)

print(acc1)