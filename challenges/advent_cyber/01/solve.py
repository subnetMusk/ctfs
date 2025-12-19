import binascii
import base64

def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int(binascii.hexlify(text.encode(encoding, errors)), 16))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return int2bytes(n).decode(encoding, errors)

def int2bytes(i):
    hex_string = '%x' % i
    n = len(hex_string)
    return binascii.unhexlify(hex_string.zfill(n + (n & 1)))

with open("start.txt", "r") as f:
    content = f.read()

letters = content.split(" ")

string = ""
for l in letters:
    string += text_from_bits(l)
# print(string) 59334e6b6531637a62474d7762544e664f474644533138334d4639685a48597a546a64664d6a41794e58303d

b64 = bytes.fromhex(string)
# print(b64) b'Y3Nke1czbGMwbTNfOGFDS183MF9hZHYzTjdfMjAyNX0='

flag = base64.b64decode(b64)
print(flag.decode("ascii"))
#csd{W3lc0m3_8aCK_70_adv3N7_2025}