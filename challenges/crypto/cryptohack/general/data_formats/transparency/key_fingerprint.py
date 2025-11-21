from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend

with open("pubkey.pem","rb") as f:
    pub = serialization.load_pem_public_key(f.read(), backend=default_backend())

spki_der = pub.public_bytes(
    encoding=serialization.Encoding.DER,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)
import hashlib, binascii
target_fp = hashlib.sha256(spki_der).hexdigest()
print("TARGET SPKI SHA256 =", target_fp)