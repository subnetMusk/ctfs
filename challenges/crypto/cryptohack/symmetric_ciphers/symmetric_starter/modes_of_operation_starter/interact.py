'''
from Crypto.Cipher import AES


KEY = ?
FLAG = ?


@chal.route('/block_cipher_starter/decrypt/<ciphertext>/')
def decrypt(ciphertext):
    ciphertext = bytes.fromhex(ciphertext)

    cipher = AES.new(KEY, AES.MODE_ECB)
    try:
        decrypted = cipher.decrypt(ciphertext)
    except ValueError as e:
        return {"error": str(e)}

    return {"plaintext": decrypted.hex()}


@chal.route('/block_cipher_starter/encrypt_flag/')
def encrypt_flag():
    cipher = AES.new(KEY, AES.MODE_ECB)
    encrypted = cipher.encrypt(FLAG.encode())

    return {"ciphertext": encrypted.hex()}


AES mode ECB, or Electronic Codebook, is the simplest AES mode where
each 128-bit block of plaintext is encrypted independently using the
same key. This makes identical plaintext blocks produce identical
ciphertext blocks, which reveals patterns and is a significant security
weakness
'''

# crypto{bl0ck_c1ph3r5_4r3_f457_!}






