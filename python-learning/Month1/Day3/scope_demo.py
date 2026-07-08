def greet(name="Guest"):
    print(f"Hello {name}")

greet()
greet("New")

def add(a: float, b: float) -> float:
    return a + b

number = add(1.5, 2.5)

print(f"{number}")

def addd(a,b):
    """
    This function adds two numbers
    
    Args:
        a: first number
        b: second number
        
    Returns:
        int: sum of a and b
    """
    return a + b

number1 = addd(1,2)
print(f"{number1}")