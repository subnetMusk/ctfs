import json
from pwn import remote

import base64
import codecs

# ---------- decoder helpers: TUTTI -> str ----------
def _bytes_to_text(b: bytes) -> str:
    return b.decode("utf-8", errors="replace")

def b64decode(s: str) -> str:
    pad = (-len(s)) % 4
    if pad:
        s += "=" * pad
    return _bytes_to_text(base64.b64decode(s, validate=False))

def hexdecode(s: str) -> str:
    cleaned = s.replace(" ", "").replace("0x", "").replace("\\x", "")
    return _bytes_to_text(bytes.fromhex(cleaned))

def rot13decode(s: str) -> str:
    return codecs.decode(s, "rot_13")

def bigintdecode(s: str) -> str:
    # interpreta "123", "0x4142", ecc.
    n = int(s, 0)
    if n == 0:
        return "\x00"
    length = (n.bit_length() + 7) // 8
    return _bytes_to_text(n.to_bytes(length, "big"))

def utf8decode(message: list) -> str:
    res = ""
    for item in message:
        res += chr(item)
    return res

DECODERS = {
    "base64": b64decode,
    "hex":    hexdecode,
    "rot13":  rot13decode,
    "bigint": bigintdecode,
    "utf-8":  utf8decode,
}

# ---------- connessione ----------
r = remote('socket.cryptohack.org', 13377, level='debug')

def json_recv():
    line = r.recvline()
    return json.loads(line.decode())

def json_send(hsh):
    # Assicurati che i valori siano serializzabili (stringhe)
    r.sendline(json.dumps(hsh).encode())

# ---------- loop di soluzione ----------
# ---------- loop corretto ----------
try:
    while True:
        received = json_recv()  # 1) leggi UN task
        enc_type = received.get("type")
        enc_value = received.get("encoded", "")

        print(f"Received type: {enc_type}")
        print(f"Received encoded value: {enc_value}")

        # 2) decodifica
        decoder = DECODERS.get(enc_type, lambda x: str(x))
        decoded = decoder(enc_value)  # deve tornare str

        # 3) invia la risposta e STOP: non leggere altro qui!
        json_send({"decoded": decoded})

        # niente json_recv() qui! il prossimo task arriverà
        # e verrà letto al prossimo ciclo
except EOFError:
    # server ha chiuso: fine challenge
    pass
finally:
    r.close()
