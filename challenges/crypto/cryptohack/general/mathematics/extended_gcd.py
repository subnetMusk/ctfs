'''
Let a and b be positive integers.

The extended Euclidean algorithm is an efficient way to find integers u,v such that

a⋅u+b⋅v=gcd(a,b)

Later, when we learn to decrypt RSA ciphertexts, we will need this algorithm to calculate
the modular inverse of the public exponent.

Using the two primes p=26513,q=32321, find the integers u,v such that

p⋅u+q⋅v=gcd(p,q)

Enter whichever of u and v is the lower number as the flag.

Knowing that p,q are prime, what would you expect gcd(p,q) to be?
For more details on the extended Euclidean algorithm, check out this page.
'''

def extended_gcd(a, b):
    # Assumo a, b >= 0
    r0, r1 = a, b
    x0, x1 = 1, 0   # coeff. su a
    y0, y1 = 0, 1   # coeff. su b

    while r1 != 0:
        q = r0 // r1            # quoziente intero
        (r0, r1) = (r1, r0 - q*r1)
        (x0, x1) = (x1, x0 - q*x1)
        (y0, y1) = (y1, y0 - q*y1)

    # r0 = gcd(a,b) e (x0, y0) sono i coefficienti
    return r0, x0, y0

print(extended_gcd(26513, 32321))

