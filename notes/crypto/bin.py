from typing import List

# -------------------------
# Step 1: string -> list ord
# -------------------------
def str_to_ord_list(s: str) -> List[int]:
    """Converte una stringa in lista di code-point (byte UTF-8)."""
    # Se vuoi i code-point Unicode (non byte), usa: [ord(c) for c in s]
    return list(s.encode("utf-8"))

# -------------------------
# Step 2: list ord -> list bin
# -------------------------
def ord_list_to_bin_list(nums: List[int], bits: int = 8) -> List[str]:
    """Converte una lista di interi in liste di stringhe binarie zfillate."""
    if bits <= 0:
        raise ValueError("bits deve essere > 0")
    out = []
    for n in nums:
        if n < 0:
            raise ValueError("Valori negativi non consentiti")
        # opzionale: limita al range dei bits
        max_val = (1 << bits) - 1
        if n > max_val:
            raise ValueError(f"Valore {n} non rappresentabile con {bits} bit")
        out.append(format(n, f"0{bits}b"))
    return out

# -------------------------
# Step 3: list bin -> bin string
# -------------------------
def bin_list_to_bin_string(bins: List[str], sep: str = "") -> str:
    """Concatena una lista di stringhe binarie in un'unica bin string."""
    # Valida che siano binarie
    for b in bins:
        if any(ch not in "01" for ch in b):
            raise ValueError(f"Stringa non binaria rilevata: {b!r}")
    return sep.join(bins)

# -------------------------
# Inverse A: bin string -> list bin
# -------------------------
def bin_string_to_bin_list(bstr: str, bits: int = 8) -> List[str]:
    """Divide una bin string in chunk di 'bits' (ignora spazi/underscore)."""
    cleaned = "".join(ch for ch in bstr if ch in "01")
    if len(cleaned) % bits != 0:
        raise ValueError(f"Lunghezza {len(cleaned)} non multipla di {bits}")
    return [cleaned[i:i+bits] for i in range(0, len(cleaned), bits)]

# -------------------------
# Inverse B: list bin -> list ord
# -------------------------
def bin_list_to_ord_list(bins: List[str]) -> List[int]:
    """Converte ogni stringa binaria in intero."""
    out = []
    for b in bins:
        if any(ch not in "01" for ch in b):
            raise ValueError(f"Stringa non binaria rilevata: {b!r}")
        out.append(int(b, 2))
    return out

# -------------------------
# Inverse C: list ord -> string
# -------------------------
def ord_list_to_str(nums: List[int]) -> str:
    """Converte una lista di byte in stringa UTF-8."""
    # Se i tuoi nums sono code-point Unicode, usa: "".join(chr(n) for n in nums)
    return bytes(nums).decode("utf-8", errors="strict")

# -------------------------
# One-shot helpers (string <-> bin string)
# -------------------------
def encode_to_bin_string(s: str, bits: int = 8, sep: str = "") -> str:
    """string -> list ord -> list bin -> bin string"""
    return bin_list_to_bin_string(
        ord_list_to_bin_list(
            str_to_ord_list(s), bits=bits
        ),
        sep=sep
    )

def decode_from_bin_string(bstr: str, bits: int = 8) -> str:
    """bin string -> list bin -> list ord -> string"""
    return ord_list_to_str(
        bin_list_to_ord_list(
            bin_string_to_bin_list(bstr, bits=bits)
        )
    )
