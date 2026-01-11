# bad_code.py

def calculate_area(radius):
    x = 3.14
    # Error 1: Logic error (using = instead of == for comparison)
    if radius == 0: 
        return 0
    
    # Error 2: Syntax error (missing closing parenthesis)
    return x * (radius ** 2) 

if __name__ == "__main__":
    calculate_area()