
class User:
    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.__password = password
    @property    
    def password(self)->str:
        return self.__password

    @password.setter
    def password(self,value:str)->None:
        self.__password = value    

class Account(User):
    def __init__(self,username:str,password:str,balance:float)->None:
        self.balance = balance
        self.history = []
        super().__init__(username,password)    


acc1 = Account("Pattapon",5555,10000.0)
print(acc1.username)
print(acc1._User__password)
print(acc1.balance)
print(acc1.history)

acc2 = Account("Somsak","1111",20000.0)
print(acc2.username)
print(acc2._User__password)
print(acc2.balance)
print(acc2.history)

acc1.password = "9999"
print(acc1.password)



