import pwn
import functools
import math

# ---------
# Source - https://stackoverflow.com/a
# Posted by President James K. Polk, modified by community. See post 'Timeline' for change history
# Retrieved 2025-11-18, License - CC BY-SA 3.0

def egcd(a, b):
    """Extended gcd of a and b. Returns (d, x, y) such that
    d = a*x + b*y where d is the greatest common divisor of a and b."""
    x0, x1, y0, y1 = 1, 0, 0, 1
    while b != 0:
        q, a, b = a // b, b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return a, x0, y0


def inverse(a, n):
    """Returns the inverse x of a mod n, i.e. x*a = 1 mod n. Raises a
    ZeroDivisionError if gcd(a,n) != 1."""
    d, a_inv, n_inv = egcd(a, n)
    if d != 1:
        raise ZeroDivisionError('{} is not coprime to {}'.format(a, n))
    else:
        return a_inv % n


def lcm(*x):
    """
    Returns the least common multiple of its arguments. At least two arguments must be
    supplied.
    :param x:
    :return:
    """
    if not x or len(x) < 2:
        raise ValueError("at least two arguments must be supplied to lcm")
    lcm_of_2 = lambda x, y: (x * y) // math.gcd(x, y)
    return functools.reduce(lcm_of_2, x)


def carmichael_pp(p, e):
    phi = pow(p, e - 1) * (p - 1)
    if (p % 2 == 1) or (e >= 2):
        return phi
    else:
        return phi // 2


def carmichael_lambda(pp):
    """
    pp is a sequence representing the unique prime-power factorization of the
    integer whose Carmichael function is to be computed.
    :param pp: the prime-power factorization, a sequence of pairs (p,e) where p is prime and e>=1.
    :return: Carmichael's function result
    """
    return lcm(*[carmichael_pp(p, e) for p, e in pp])
# ---------------



e = 65537
N =24298033422017060514241339496181557513780024457418471689934217912074681661871841347721535817924614480103837434601240692089791440280948221313383706916075118

cipher_text = 5784145235789221831010167711276373116165233657507925738800127595778087337935057972095476980814361570126735929074857304085694384033930477270254976560000261

lam = carmichael_lambda([(2,8), (N, 1)])
z = inverse(e, lam)
x = pow(cipher_text, z, N)

plain_bytes = x.to_bytes((x.bit_length() + 7) // 8, byteorder='little')

plain = plain_bytes.decode('ascii')


chars = []
for p in plain:
    chars.insert(0, p)

flag = ''.join(chars)

print(flag)