day = 2

match day:
    case 1:
        print("Monday")
    case 2:
        print("Tuesday")
    case _:
        print("Unknown")


manu = input("Enter your manu: ")

match manu:
    case 1:
        print("Pizza")
    case 2:
        print("Burger")
    case _:
        print("Coffee")
