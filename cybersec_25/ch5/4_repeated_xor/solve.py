from collections import Counter
import itertools


def shift_bytes(enc_b, shift):
    return enc_b[shift:] + enc_b[:shift]

def count_same_spot(b1, b2):
    count = 0
    for i in range(len(b1)):
        if b1[i] == b2[i]:
            count += 1
    return count

def xor(bt1, bt2):
    return bytes(bt1 ^ bt2 for b1, b2 in zip(bt1, bt2))


with open("encrypted.txt") as f:
    encrypted = f.read()

enc_bytes = bytes.fromhex(encrypted)

freq = {}
for i in range(5, 15):
    copy = shift_bytes(enc_bytes, i)
    freq[i] = count_same_spot(enc_bytes, copy)

#print(freq)
# key len = 8

key_len = 8
blocks = []

key = []
for i in range(key_len):
    block = enc_bytes[i::key_len]
    blocks.append(block)
    best_byte = Counter(block).most_common(1)[0][0]
    key.append(best_byte ^ ord(' '))

final_key = bytes(key)

decrypted = []
for cipher_byte, key_byte in zip(enc_bytes, itertools.cycle(final_key)):
    decrypted.append(cipher_byte ^ key_byte)

flag = ""
for d in decrypted:
    flag+=chr(d)

print(flag)

#your flag is: 8eb31c92334eac8f6dacfbaaa5e40294a31e66e0














