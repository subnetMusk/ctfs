import base64

cipher_text = 'fYZ7ipGIjFtsXpNLbHdPbXdaam1PS1c5lQ=='

cipher_bytes = base64.b64decode(cipher_text)

for shift in range(256):
    flag_b = bytes([(b + shift) % 256 for b in cipher_bytes])
    flag_c = flag_b.decode('ascii', errors='ignore')
    if "{" not in flag_c:
        continue
    else:
        print(flag_c)

# encryptCTF{3T_7U_BRU73?!}