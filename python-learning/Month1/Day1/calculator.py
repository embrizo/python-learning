#Enter Number 1
#Enter Number 2
#Operation (+, -, *, /)

Number1 = float(input("Enter Number 1: "))
Number2 = float(input("Enter Number 2: "))
Operation = input("Enter Operation (+, -, *, /): ")

if Operation == "+":
    print("Result: ", Number1 + Number2)
elif Operation == "-":
    print("Result: ", Number1 - Number2)
elif Operation == "*":
    print("Result: ", Number1 * Number2)
elif Operation == "/":
    print("Result: ", Number1 / Number2)
else:
    print("Invalid Operation")

print("___________________")
print("Every Operation")
print("___________________")
print("Result:", Number1 + Number2, "\n")
print("Result:", Number1 - Number2, "\n")
print("Result:", Number1 * Number2, "\n")
print("Result:", Number1 / Number2, "\n")
print("___________________")
