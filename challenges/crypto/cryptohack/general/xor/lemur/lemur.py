'''
I've hidden two cool images by XOR with the same secret key so you can't see them!

This challenge requires performing a visual XOR between the RGB bytes of the two images -
not an XOR of all the data bytes of the files.
'''

from PIL import Image
import numpy as np


A_PATH = "lemur_ed66878c338e662d3473f0d98eedbd0d.png"
B_PATH = "flag_7ae18c704272532658c10b5faad06d74.png"
OUT    = "flag.png"

A = Image.open(A_PATH).convert("RGB")
B = Image.open(B_PATH).convert("RGB")

# croppiamo all'intersezione minima
w = min(A.width, B.width)
h = min(A.height, B.height)
if (A.size != (w,h)) or (B.size != (w,h)):
    A = A.crop((0, 0, w, h))
    B = B.crop((0, 0, w, h))

# 3) XOR per canale (uint8)
a = np.array(A, dtype=np.uint8)
b = np.array(B, dtype=np.uint8)

# XOR RGB
x = np.bitwise_xor(a, b)

# 4) Salva
Image.fromarray(x, mode="RGB").save(OUT)
print(f"Salvato: {OUT}")



