'''
As we've seen, we can work within a finite field Fp,
adding and multiplying elements, and always obtain another element of the field.

For all elements g in the field, there exists a unique integer d such that
g⋅d ≡ 1 mod p.

This is the multiplicative inverse of g.

Example: 7⋅8= 56 ≡ 1 mod 11

What is the inverse element: d=3−1 such that
3⋅d ≡ 1 mod 13?

Think about the little theorem we just worked with.
How does this help you find the inverse of an element?
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

a = 3
b = 1
n = 13

a = a % n

ext = extended_gcd(a, n)

if ext[0] == 1:
    res = ext[1] % n
    print(res)


