def celsius_to_fahrenheit():
    c = int(input("Input Celsius = "))
    f = 9/5*c + 32
    return f


def fahrenheit_to_celsius():
    f = int(input("Input Fahrenheit = "))
    c = (f - 32) * 5/9
    return c