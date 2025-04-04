def prime(n):
    for i in range(2, int(n**.5)+1): # loops through 2 till n - 1
        if n % i == 0: # checks if its divisible by those numbers
            return False
    return True

