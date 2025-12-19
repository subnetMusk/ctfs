import base64
from Crypto.Cipher import AES
from Crypto.Hash import MD5, SHA256
from Crypto.Protocol.KDF import PBKDF2, scrypt
import struct
import sys

# --- Dettagli del Puzzle ---
# Stringa cifrata (formato Base64 OpenSSL)
CIPHERTEXT_OPENSSL = "U2FsdGVkX18bFYOs0Qxt4NjMQ5g+lxOzbOuCRB2RG3Q2fw4mKC93xKIpFnH8Mo6h"
# Target per la validazione (la "flag" di successo nel codice JS)
TARGET_STRING = "Answer Correct"
# Il puzzle sblocca il contenuto successivo, quindi questo è il target alternativo, ma non è necessario per la forza bruta:
# TARGET_SUBSEQUENT_JSON_START = '{"title":'
# In questo caso, ci concentriamo sulla stringa di successo del puzzle attuale.

# --- Parametri AES EvpKDF ---
# CryptoJS usa 256-bit key (32 bytes) e 128-bit IV (16 bytes) per l'AES.
KEY_SIZE = 32  # 256 bits
IV_SIZE = 16  # 128 bits
ITERATIONS = 1  # EvpKDF (come usato da CryptoJS di default) esegue una sola iterazione.
HASHER = MD5  # EvpKDF di CryptoJS di default usa MD5 per derivare la chiave e il salt.


def evp_bytes_to_key(password: str, salt: bytes, key_len: int, iv_len: int, iterations: int, hasher):
    """
    Implementazione del metodo OpenSSL EvpKDF per derivare la chiave e l'IV.
    Simula il comportamento di CryptoJS/OpenSSL.
    """
    key_iv = b''
    last_hash = b''

    while len(key_iv) < (key_len + iv_len):
        hasher_obj = hasher.new(last_hash + password.encode('utf-8') + salt)
        last_hash = hasher_obj.digest()
        key_iv += last_hash

    return key_iv[:key_len], key_iv[key_len:key_len + iv_len]


def decrypt_aes_openssl(ciphertext_openssl_b64: str, password: str) -> str:
    """
    Decifra una stringa AES nel formato OpenSSL.
    """
    try:
        # Decodifica Base64
        data = base64.b64decode(ciphertext_openssl_b64)
    except Exception:
        return ""

    # Verifica il magic header (Salted__)
    if data[:8] != b'Salted__':
        # Se non ha l'header, potremmo tentare la decifratura diretta,
        # ma per la CTF ci aspettiamo il formato OpenSSL.
        return ""

    # Estrae il Salt e il Ciphertext
    salt = data[8:16]
    ciphertext_raw = data[16:]

    # Deriva Key e IV usando EvpKDF
    key, iv = evp_bytes_to_key(password, salt, KEY_SIZE, IV_SIZE, ITERATIONS, HASHER)

    # Crea il cifratore AES in modalità CBC
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Decifra e rimuovi il padding PKCS#7 (CryptoJS lo fa di default)
    decrypted_padded = cipher.decrypt(ciphertext_raw)

    # Rimozione del padding PKCS#7 (implementazione manuale per la compatibilità)
    try:
        padding_length = decrypted_padded[-1]
        if padding_length > AES.block_size or padding_length == 0:
            raise ValueError

        # Verifica che gli ultimi N byte siano tutti uguali al valore di padding
        if all(decrypted_padded[-padding_length] == padding_length for byte in decrypted_padded[-padding_length:]):
            decrypted_text = decrypted_padded[:-padding_length].decode('utf-8')
        else:
            # Padding non valido
            raise ValueError

    except (IndexError, ValueError):
        return "Decryption Error: Invalid Padding/Data"

    return decrypted_text


def bruteforce_7_digit_key():
    print(f"--- Inizio Brute-Force AES (Chiave: 7 cifre, Target: '{TARGET_STRING}') ---")
    print("Saranno testate 10.000.000 combinazioni. Potrebbe volerci del tempo.")

    for i in range(10000000):
        # La chiave è la stringa del numero (es. "0012345")
        key_num = str(i).zfill(7)

        # Simula la normalizzazione (che per soli numeri non cambia nulla)
        key_normalized = key_num

        decrypted = decrypt_aes_openssl(CIPHERTEXT_OPENSSL, key_normalized)

        if "Answer Correct" in decrypted:
            print("\n" + "=" * 50)
            print(f"🎉 RISPOSTA TROVATA!")
            print(f"La chiave (risposta corretta) è: {key_num}")
            print("=" * 50)
            return key_num

        # Stato di avanzamento (opzionale, per evitare di attendere a vuoto)
        if i % 100000 == 0:
            sys.stdout.write(f"\rTentativi: {i:,} - Ultima chiave: {key_num}")
            sys.stdout.flush()

    print("\n" + "-" * 50)
    print("❌ Brute-Force completato. Chiave non trovata nell'intervallo 0-9999999.")
    print("-" * 50)
    return None


if __name__ == "__main__":
    bruteforce_7_digit_key()