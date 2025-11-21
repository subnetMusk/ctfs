from pwn import *          # pip install pwntools
import json

r = remote('socket.cryptohack.org', 13372, level='debug')

def recv_line_text():
    return r.recvline().decode().strip()

def send_json(obj):
    r.sendline(json.dumps(obj).encode())

# 1) Leggi banner e ignoralo
banner = recv_line_text()

# 2) Prendi il ciphertext del flag
send_json({"option": "get_flag"})
resp = json.loads(recv_line_text())
enc_hex = resp["encrypted_flag"]           # esadecimale
C = bytes.fromhex(enc_hex)                 # bytes del ciphertext

# 3) Chiedi di cifrare zeri della stessa lunghezza => ottieni la chiave K
zeros_hex = ("00" * len(C))               # stringa esadecimale di zeri
send_json({"option": "encrypt_data", "input_data": zeros_hex})

resp2 = json.loads(recv_line_text())
# alcune istanze ritornano con chiavi diverse; prova in ordine:
ct2_hex = (resp2.get("ciphertext")
           or resp2.get("encrypted_data")
           or resp2.get("data")
           or resp2.get("encrypted_flag"))
K = bytes.fromhex(ct2_hex)

# 4) Recupera il flag: C ⊕ K
from pwnlib.util.fiddling import xor
flag_bytes = xor(C, K)

print(flag_bytes.decode(errors="ignore"))
r.close()
