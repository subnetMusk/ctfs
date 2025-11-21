'''
For the next few challenges, you'll use what you've just learned to solve some
more XOR puzzles.

I've hidden some data using XOR with a single byte, but that byte is a secret.
Don't forget to decode from hex first.

73626960647f6b206821204f21254f7d694f7624662065622127234f726927756d
'''

from pwn import xor
import re

string_h = "73626960647f6b206821204f21254f7d694f7624662065622127234f726927756d"
string = bytes.fromhex(string_h)

for key in range(256):
    p = xor(string, bytes([key]))
    res = p.decode('utf-8', errors='ignore')
    m = re.match(r"^crypto{*", res)
    if m:
        print(res)
        break

