'''
from Crypto.Cipher import AES
import hashlib
import random


# /usr/share/dict/words from
# https://gist.githubusercontent.com/wchargin/8927565/raw/d9783627c731268fb2935a731a618aa8e95cf465/words
with open("/usr/share/dict/words") as f:
    words = [w.strip() for w in f.readlines()]
keyword = random.choice(words)

KEY = hashlib.md5(keyword.encode()).digest()
FLAG = ?


@chal.route('/passwords_as_keys/decrypt/<ciphertext>/<password_hash>/')
def decrypt(ciphertext, password_hash):
    ciphertext = bytes.fromhex(ciphertext)
    key = bytes.fromhex(password_hash)

    cipher = AES.new(key, AES.MODE_ECB)
    try:
        decrypted = cipher.decrypt(ciphertext)
    except ValueError as e:
        return {"error": str(e)}

    return {"plaintext": decrypted.hex()}


@chal.route('/passwords_as_keys/encrypt_flag/')
def encrypt_flag():
    cipher = AES.new(KEY, AES.MODE_ECB)
    encrypted = cipher.encrypt(FLAG.encode())

    return {"ciphertext": encrypted.hex()}

---- ONLINE VERSION ----
import requests
import hashlib
import json

se = requests.Session()
words_dict = se.get("https://gist.githubusercontent.com/wchargin/8927565/raw/d9783627c731268fb2935a731a618aa8e95cf465/words").text.split("\n")
dict_len = len(words_dict)

target = "https://aes.cryptohack.org/passwords_as_keys/"
enc_flag = json.loads(se.get(target+"encrypt_flag/").text)["ciphertext"]

for i,w in enumerate(words_dict):
    h = hashlib.md5(w.encode()).digest().hex()
    g = f"decrypt/{enc_flag}/{h}/"
    guess = json.loads(se.get(target+g).text)
    if "plaintext" in guess:
        plain = bytes.fromhex(guess["plaintext"]).decode("latin")
        print(f"=={i}/{dict_len}==\nPLAIN: {plain}\nHASH: {h}\n======\n")
        if "cryptohack{" in plain:
            break

'''

# ---- OFFLINE VERSION ----
import requests
import hashlib
from Crypto.Cipher import AES

# Setup sessione
se = requests.Session()
target = "https://aes.cryptohack.org/passwords_as_keys/"

# 1. Scarica il dizionario
print("[*] Scaricamento dizionario...")
words_url = "https://gist.githubusercontent.com/wchargin/8927565/raw/d9783627c731268fb2935a731a618aa8e95cf465/words"
words_list = se.get(words_url).text.splitlines()  # splitlines() gestisce meglio \n e \r\n
print(f"[*] Caricate {len(words_list)} parole.")

# 2. Ottieni la Flag cifrata (una sola volta)
print("[*] Recupero flag cifrata...")
r = se.get(target + "encrypt_flag/")
ciphertext_hex = r.json()["ciphertext"]
ciphertext_bytes = bytes.fromhex(ciphertext_hex)

print("[*] Avvio Brute Force Offline...")

# 3. Loop ottimizzato
for i, word in enumerate(words_list):
    word = word.strip()
    if not word:
        continue
    # Hash MD5 della parola (la chiave è a 128 bit / 16 byte)
    # NOTA: Usiamo direttamente i bytes, niente hex inutile
    key = hashlib.md5(word.encode()).digest()

    cipher = AES.new(key, AES.MODE_ECB)

    try:
        decrypted = cipher.decrypt(ciphertext_bytes)

        # Check rapido sulla flag nota
        if b"crypto" in decrypted:
            print(f"\n[SUCCESS] Trovata alla riga {i}!")
            print(f"KEY (word): {word}")
            print(f"FLAG: {decrypted.decode('utf-8')}")
            break

    except ValueError:
        continue

    # Feedback visuale opzionale ogni 5000 tentativi per non rallentare
    if i % 5000 == 0:
        print(f"\rProgress: {i}/{len(words_list)}", end="")