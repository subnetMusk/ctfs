import binascii


with open("secret.enc", "rb") as f:
    secret = f.read()

with open("password.enc", "rb") as f:
    password = f.read()

message = secret.hex()

password = binascii.unhexlify(password)

p_hex = password.hex()

# NOT DONE
