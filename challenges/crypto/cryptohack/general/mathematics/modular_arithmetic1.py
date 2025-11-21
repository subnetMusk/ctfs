'''
Imagine you lean over and look at a cryptographer's notebook.
You see some notes in the margin:

4 + 9 = 1
5 - 7 = 10
2 + 3 = 5

At first you might think they've gone mad.
Maybe this is why there are so many data leaks nowadays you'd think,
but this is nothing more than modular arithmetic modulo 12 (albeit with some sloppy
notation).

You may not have been calling it modular arithmetic, but you've been doing these
kinds of calculations since you learnt to tell the time
(look again at those equations and think about adding hours).

Formally, "calculating time" is described by the theory of congruences.
We say that two integers are congruent modulo m if a≡b mod m.

Another way of saying this, is that when we divide the integer aa by m,
the remainder is b.
This tells you that if m divides a (this can be written as m∣a) then
a≡ 0 mod m

Calculate the following integers:

11 ≡ x mod 6
8146798528947 ≡ y mod 17

The solution is the smaller of the two integers, (x,y), you obtained after
reducing by the modulus.
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

def reduced_module(a, m):
    if m <= 0:
        return -1
    if m == 1:
        return 0
    return a%m

# caso 1:
print(reduced_module(11, 6))

#caso 2:
print(reduced_module(8146798528947, 17))

