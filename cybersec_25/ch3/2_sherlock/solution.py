import binascii

flag = ""

with open("challenge.txt") as f:
    while True:
        c = str(f.read(1))
        if c.isupper():
            flag += c

        if not c:
            break

print(flag)

flag2 = str.replace(flag, "ZERO", '0')
flag2 = str.replace(flag2, "ONE", '1')

print(flag2)

s = ''.join(chr(int(flag2[i:i+8], 2)) for i in range(0, len(flag2), 8))
print(s)

