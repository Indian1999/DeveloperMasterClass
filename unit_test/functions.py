def add(a, b):
    return a + b

def power(a, b):
    if a == 0 and b == 0:
        raise(ValueError("0^0 is undefined!"))
    return a ** b

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero!")