# https://www.geeksforgeeks.org/sieve-eratosthenes-0n-time-complexity/
def getSieve(n):
    """Returns array with prime numbers up to n.
    Computes such array in O(n) time/space using Sieve of Eratosthenes"""

    isprime = [True for _ in range(n)]  
    prime = []  
    spf = [None for _ in range(n)]
        
    isprime[0] = isprime[1] = False
    for i in range(2, n):
        if isprime[i]:
            prime.append(i)
            spf[i] = i
                
        j = 0
        while (j < len(prime) and i * prime[j] < n and prime[j] <= spf[i]):
            isprime[i * prime[j]] = False
            spf[i * prime[j]] = prime[j] 
                
            j += 1

    return prime

def is_probably_prime(n, sieve):
    for x in sieve:
        if n % x == 0:
            return False
    return True

def gcd(a, b):
    """Euclid's algorithm for GCD
    Given input a, b the function returns d such that gcd(a,b) = d"""

    if a < b:
        a,b = b,a

    while b != 0:
        a, b = b, a % b
    return a

def modpow(x, y, p):
    x %= p
    if x == 0: return 0

    res = 1 
    while y > 0:
        if y & 1: res = (res * x) % p

        y >>= 1
        x = (x * x) % p         
    return res

import random, math
def generatePrime(n : int, primes = None, s = None):
    """Generates prime number with at least n digits:

    : param n: number of 10-based digits in the generate prime is at least n;
    : param primes: iterable object of numbers that are used as small factors
    for pre-prime verification. If None, is computed using getSieve(1000);
    : param s: initial prime number - if None, last from primes is used;
    """

    # Any prime number higher than the up_limit suffices the result.
    up_limit = 10**n

    # Get the list of small primes which are used as small divisors
    # to reject the n candidate before the Pocklington test.
    if not primes: primes = getSieve(1000)

    if not s: s = primes[-1] # initial prime
    while s < up_limit:
        lo, hi = (s + 1) >> 1, 2*s + 1

        # Proceed with finding new prime n
        while True:
            r = random.randint(lo, hi) << 1 # get random even r from [s, 4*s + 2]
            n = s*r + 1 # n is prime candidate, s^2 + 1 <= n <= 4s^2 + 2s + 1

            # reject n if n divides some number in primes list
            if not is_probably_prime(n, primes): continue

            # Here n is probably prime - apply Pocklington criterion to verify it
            while True:
                a = random.randint(2, n-1)

                # Fermat’s little theorem isn't satisfied - choose another n
                if pow(a, n-1, n) != 1: 
                    break

                d = math.gcd((pow(a, r, n) - 1) % n, n)
                if d != n:
                    if d == 1: s = n # n is prime, replace s with n
                    else: pass # n isn't prime, choose another n
                    break
                else: pass # a^r mod n == 1, choose another a
            if s == n: break
    return s

import sympy
def test(n, k):
    primes = getSieve(1000)
    for x in range(n >> 1, n):
        print(x)
        for _ in range(k):
            assert sympy.ntheory.primetest.isprime(generatePrime(x, primes))

if __name__ == '__main__':
    #test(20, 10000)

    prime_num = generatePrime(50)
    prime = str(prime_num)
    print(prime, len(prime))
    #assert sympy.ntheory.primetest.isprime(prime_num)