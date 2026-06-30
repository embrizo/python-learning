#Coin
#Quantity
#Buy Price

Coin = input("Enter your Coin: ")
Quantity = float(input("Enter your Quantity: "))
Buy_Price = float(input("Enter your Buy Price: "))

Current_Price = float(input("Enter your Current Price: "))

print("============================")
print("Portfolio Summary")
print("============================")
print("Coin: ", Coin)
print("Quantity: ", Quantity)
print(f"Buy Price: {Buy_Price:.2f} THB")
print(f"Current Price: {Current_Price:.2f} THB")
print(f"Total Amount: {Quantity * Buy_Price:.2f} THB")
