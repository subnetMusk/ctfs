import itertools
import string

def vigenere_cipher(cipher, key, alphabet):
    flag = ""
    for c, k in zip(cipher, itertools.cycle(key)):
        char = alphabet[(alphabet.find(c) - alphabet.find(k)) % len(alphabet)]
        print(char)
        flag += char
    return flag


cipher_text = "vhixoieemksktorywzvhxzijqni"

alfabeto = string.ascii_lowercase

print(vigenere_cipher(cipher_text, "caesar", alfabeto))

#theforceisstrongwiththisone