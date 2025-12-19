import requests
import json
import binascii

target = "https://aes.cryptohack.org/ecbcbcwtf"
conn = requests.Session()

flag_req = conn.get(target+"/encrypt_flag")
flag_res = json.loads(flag_req.text)

IV_hex = flag_res['ciphertext'][:32]
IV = binascii.unhexlify(IV_hex)

ciphertext = flag_res['ciphertext'][32:]
cipher_bytes = bytes.fromhex(ciphertext)

dec_req = conn.get(target+"/decrypt/"+ciphertext)
dec_res = json.loads(dec_req.text)

dec_bytes = bytes.fromhex(dec_res['plaintext'])

blocks = []
flag = bytearray()
for i in range(len(dec_bytes) // 16):
    if i == 0:
        flag += bytes(a ^ b for a,b in zip(dec_bytes[i*16:(i+1)*16], IV))
    else:
        flag += bytes(a ^ b for a,b in zip(dec_bytes[i*16:(i+1)*16], cipher_bytes[(i-1)*16:i*16]))

print(flag.decode("latin"))

# crypto{3cb_5uck5_4v01d_17_!!!!!}