from __future__ import annotations
import base64
import codecs
from typing import Callable, Dict

# ---------- helpers ----------

def _bytes_to_text(b: bytes) -> str:
    """Converte bytes->str (UTF-8, sostituendo i byte non validi)."""
    return b.decode("utf-8", errors="replace")

def _text_to_bytes(s: str) -> bytes:
    """Converte str->bytes (UTF-8)."""
    return s.encode("utf-8")

def _normalize_hex(s: str) -> str:
    """Rimuove spazi e prefissi comuni (0x, \\x) dalla stringa esadecimale."""
    s = s.strip().replace(" ", "")
    # sostituisci sequenze \xNN (anche ripetute)
    s = s.replace("\\x", "")
    # rimuovi '0x' iniziale (singolo)
    if s.lower().startswith("0x"):
        s = s[2:]
    return s

def _pad_base64(s: str) -> str:
    """Aggiunge '=' mancanti per rendere la lunghezza multipla di 4."""
    pad = (-len(s)) % 4
    return s + ("=" * pad if pad else "")


def _rotN_char(c: str, n: int) -> str:
    """Ruota una singola lettera ASCII di n posizioni (mod 26).
    Mantiene case; non-letters restano inalterati.
    """
    if 'a' <= c <= 'z':
        base = ord('a')
        return chr(base + ((ord(c) - base + n) % 26))
    if 'A' <= c <= 'Z':
        base = ord('A')
        return chr(base + ((ord(c) - base + n) % 26))
    return c

# ---------- BASE64 ----------

def b64_encode(text: str) -> str:
    """text -> base64 (ASCII, senza newline)."""
    return base64.b64encode(_text_to_bytes(text)).decode("ascii")

def b64_decode(b64: str) -> str:
    """base64 -> text (UTF-8; sostituisce byte illeggibili)."""
    b64 = _pad_base64(b64.strip())
    return _bytes_to_text(base64.b64decode(b64, validate=False))

# ---------- HEX ----------

def hex_encode(text: str) -> str:
    """text -> hex (minuscolo, senza '0x' né spazi)."""
    return _text_to_bytes(text).hex()

def hex_decode(h: str) -> str:
    """hex (con o senza '0x'/'\\x', spazi ammessi) -> text."""
    cleaned = _normalize_hex(h)
    return _bytes_to_text(bytes.fromhex(cleaned))

# ---------- ROT-N ----------

def rotN_encode(text: str, n: int) -> str:
    """Applica ROT-N (n può essere qualsiasi intero, anche negativo)."""
    n = n % 26  # normalizza
    return "".join(_rotN_char(c, n) for c in text)

def rotN_decode(text: str, n: int) -> str:
    """Inversa di ROT-N: equivale a ROT-(26-n)."""
    return rotN_encode(text, -n)

# ---------- BIGINT (intero rappresentato come stringa) ----------

def bigint_encode_hex(text: str, with_prefix: bool = True) -> str:
    """
    text -> '0x' + hex dei byte UTF-8 (big-endian).
    Utile per protocolli che vogliono un bigint in forma esadecimale.
    """
    hx = _text_to_bytes(text).hex()
    return ("0x" + hx) if with_prefix else hx

def bigint_decode(num: str) -> str:
    """
    '0x...' (esadecimale) o '...' (decimale) -> interpreta come intero big-endian -> text.
    Esempi validi: '0x6869', '26729'.
    """
    n = int(num.strip(), 0)  # 0 => auto base (0x..., 0o..., 0b..., dec)
    if n == 0:
        return "\x00"
    length = (n.bit_length() + 7) // 8
    return _bytes_to_text(n.to_bytes(length, "big"))

# ---------- BYTES ESCAPE (rappresentazione come stringa \xNN) ----------

def bytes_escape_encode(text: str) -> str:
    """text -> stringa con escape esadecimali tipo '\\x68\\x69' (byte UTF-8)."""
    return "".join(f"\\x{b:02x}" for b in _text_to_bytes(text))

def bytes_escape_decode(escaped: str) -> str:
    """
    '\\x68\\x69' o altre sequenze standard di escape -> text.
    Nota: interpreta anche \\n, \\t, \\uXXXX, ecc. (unicode_escape).
    """
    return codecs.decode(escaped, "unicode_escape")

