import requests
import json
import string

alphabet = string.printable

target = "https://aes.cryptohack.org/ecb_oracle/"
se = requests.Session()

# secondo me i primi byte della falg sono "crypto{"

payload_1 = "AAAAAAAAA".encode().hex()
req_plain_flag = se.get(target+"encrypt/"+payload_1+"/")
cipher_plain = json.loads(req_plain_flag.text)["ciphertext"][:32]

payload_2 = "AAAAAAAAAcrypto{".encode().hex()
req_plain_flag = se.get(target+"encrypt/"+payload_2+"/")
guess_plain = json.loads(req_plain_flag.text)["ciphertext"][:32]
assert guess_plain == cipher_plain

# direi che sono uguali

def calculate_padding(f):
    mod = (len(f)+1) % 16
    if mod == 0:
        return 0
    return 16 - mod

flag = ""
for i in range(1, 100):
    padding = str(("A"*32)+"A"*calculate_padding(flag))
    padding_hex = padding.encode().hex()

    block = ((len(padding) + len(flag)) // 16)

    req_cifrato = se.get(target+"encrypt/"+padding_hex+"/")
    cifrato = json.loads(req_cifrato.text)["ciphertext"][block*32:(block+1)*32]
    for c in alphabet:
        payload_guess = str(padding+flag+c)
        payload_guess_hex = payload_guess.encode().hex()
        req_ = se.get(target+"encrypt/"+payload_guess_hex+"/")
        out = json.loads(req_.text)["ciphertext"][block*32:(block+1)*32]
        if out == cifrato:
            flag += c
            print(flag)
            break

print(flag)