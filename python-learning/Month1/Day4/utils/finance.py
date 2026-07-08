def calculate_roi():
    p = input("Enter the principal amount: ")
    r = input("Enter the rate of interest: ")
    t = input("Enter the time in years: ")
    return (int(p)*int(r)*int(t))/100

def calculate_profit():
    invest = input(f"Enter amount Invest = ")
    now = input(f"Enter amount now price = ")
    return (int(now)-int(invest))