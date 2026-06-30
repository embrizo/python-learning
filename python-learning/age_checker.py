age = int(input("Enter your age: "))
print(f"You are {age} years old.")
print(f"age >= 18: {age >= 18}")
print(f"age < 18: {age < 18}")
print(f"age == 20: {age == 20}")
print(f"age != 20: {age != 20}")
print(f"________________________")



#Adult
#Minor
if age >= 18:
    print(f"Adult")
else:
    print(f"Minor")

print(f"________________________")

#Even
#Odd
if age % 2 == 0:
    print(f"Even")
else:
    print(f"Odd")

    age = 20
citizen = True

if age >= 18 and citizen:
    print("Can Vote")

print(f"________________________")
vip = False
member = True

if vip or member:
    print("Discount")
print(f"________________________")


score = float(input("Enter your Score: "))