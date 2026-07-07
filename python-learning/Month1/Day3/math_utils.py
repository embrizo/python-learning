def  square(x):
    return x*x

def cube(x):
    return x*x*x

def  circle_area(r):
    return 3.14 * r * r

def circle_circumference(r):
    return 2 * 3.14 * r

def fahrenheit_to_celsius(f):
    return (f - 32) * 5 / 9

s = square(5)
print(f"square of 5 is {s}")
c = cube(5)
print(f"cube of 5 is {c}")
a = circle_area(5)
print(f"Area of circle is {a}")
c = circle_circumference(5)
print(f"Circumference of circle is {c}")
f = fahrenheit_to_celsius(5)
print(f"Fahrenheit to Celsius is {f}")

