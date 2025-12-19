"""
PASSWORD GENERATOR X ALFA NUMERIC CHARS
"""

import random
import string

lunghezza = int(input("Inserire la lunghezza della password: "))

alfabeto = string.ascii_letters + string.digits

password = ""
for i in range(lunghezza):
    password += random.choice(alfabeto)

print(password)