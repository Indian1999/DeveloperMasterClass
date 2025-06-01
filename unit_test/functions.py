def add(a, b):
    return a + b

def power(a, b):
    if a == 0 and b == 0:
        raise(ValueError("0^0 is undefined!"))
    if a == 0 and b < 0:
        raise(ValueError("0 cannot be raised to a negitve power!"))
    return a ** b

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero!")
    return a / b