import requests
target_url = "http://aes.cryptohack.org/flipping_cookie/"

se = requests.session()
cookie_hex = se.get(target_url + "get_cookie/").json()
cookie_bytes = bytes.fromhex(cookie_hex["cookie"])

original_IV = cookie_bytes[:16]
original_ciphertext = cookie_bytes[16:]

'''
L'obbiettivo è far si che il cookie decifrato contenga la stringa "admin=True" + ";" (per il padding) al posto di "admin=False"
Possiamo dunque craftare un IV personalizzato per far si che l'inzio del cookie passi la verifica di auth
'''

bytearray_IV = bytearray(original_IV)
new_iv = bytearray_IV
string_o = "False"
string_t = "True;"
for n in range(6, 11):
    new_iv[n] = bytearray_IV[n] ^ ord(string_o[n-6]) ^ ord(string_t[n-6])

response = se.get(target_url + "check_admin/" + original_ciphertext.hex() + "/" + new_iv.hex()).json()
print(response)