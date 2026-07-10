from typing import Optional
from dataclasses import dataclass
@dataclass
class Transaction:
    type:str
    amount:float
    timestamp:str
    note: Optional[str] = None

    def __str__(self)->str:
        return f"{self.timestamp} - {self.type} - {self.amount} - {self.note}"

    
