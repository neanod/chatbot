def is_prime(n):
     """Checks if a number is prime."""
     if n <= 1:
         return False
     if n <= 3:
         return True
     if n % 2 == 0 or n % 3 == 0:
         return False
     i = 5
     while i * i <= n:
         if n % i == 0 or n % (i + 2) == 0:
             return False
         i += 6
     return True

def sum_of_first_n_primes(n):
    """Calculates the sum of the first n prime numbers."""
    primes = []
    num = 2
    while len(primes) < n:
        if is_prime(num):
            primes.append(num)
        num += 1
    return sum(primes)
                                                                                                                
# Calculate the sum of the first 100 prime numbers
sum_100_primes = sum_of_first_n_primes(100)
print(f"The sum of the first 100 prime numbers is: {sum_100_primes}")