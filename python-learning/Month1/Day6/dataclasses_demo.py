from importlib import resources
from abc import ABC, abstractmethod
class storage(ABC):
    @abstractmethod
    def save():
        pass

from dataclasses import dataclass
@dataclass
class User:
    name: str
    age: int

    def save(self):
        print("User saved to storage")

@dataclass
class Prompt:

    system:str

    user:str

    temperature:float        