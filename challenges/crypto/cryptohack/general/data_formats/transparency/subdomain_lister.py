import re, time, hashlib, requests, traceback, ssl, socket
from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives.asymmetric import rsa

BASE = "cryptohack.org"
PUBKEY_PATH = "transparency_afff0345c6f99bf80eab5895458d8eab.pem"
VERBOSE = True
SLEEP = 0.03
TIMEOUT = 25

def dbg(*a):
    if VERBOSE: print(*a)

# --- carica chiave target e caratterizza ---
with open(PUBKEY_PATH, "rb") as f:
    target_pub = serialization.load_pem_public_key(f.read())

spki_der = target_pub.public_bytes(
    encoding=serialization.Encoding.DER,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)
TARGET_SPKI = hashlib.sha256(spki_der).hexdigest()
dbg("[TARGET] spki_sha256 =", TARGET_SPKI)

target_nums = None
if isinstance(target_pub, rsa.RSAPublicKey):
    tn = target_pub.public_numbers()
    target_nums = (tn.n, tn.e)
    dbg(f"[TARGET] RSA bits={target_pub.key_size} e={tn.e} n[:16hex]={hex(tn.n)[:18]}...")

PEM_RE = re.compile(
    rb"-----BEGIN CERTIFICATE-----\r?\n.*?\r?\n-----END CERTIFICATE-----\r?\n?",
    re.DOTALL
)

def parse_any_cert(blob: bytes):
    # prova DER
    try:
        return [x509.load_der_x509_certificate(blob)]
    except Exception:
        pass
    # PEM concatenati
    certs = []
    for m in PEM_RE.finditer(blob):
        try:
            certs.append(x509.load_pem_x509_certificate(m.group(0)))
        except Exception:
            pass
    return certs

def extract_names(cert: x509.Certificate):
    names = []
    try:
        san = cert.extensions.get_extension_for_class(x509.SubjectAlternativeName).value
        names = san.get_values_for_type(x509.DNSName)
    except Exception:
        pass
    if not names:
        try:
            cn = cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value
            names = [cn]
        except Exception:
            pass
    return sorted(set(names))

def spki_sha256_from_cert(cert: x509.Certificate) -> str:
    pub = cert.public_key()
    spki = pub.public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return hashlib.sha256(spki).hexdigest(), pub

def fetch_ct(domain: str):
    urls = [
        f"https://crt.sh/?q=%25.{domain}&output=json",  # wildcard
        f"https://crt.sh/?q={domain}&output=json",      # nudo
    ]
    out = []
    for url in urls:
        dbg("[CT] GET", url)
        r = requests.get(url, timeout=TIMEOUT)
        dbg("[CT] status", r.status_code, "bytes", len(r.content))
        if r.ok:
            try:
                out.extend(r.json())
            except Exception:
                pass
    dbg("[CT] total entries:", len(out))
    return out

def fetch_cert_blob(cert_id: int) -> bytes:
    # &output=der per avere DER pulito; senza può tornare PEM
    url = f"https://crt.sh/?d={cert_id}&output=der"
    r = requests.get(url, timeout=TIMEOUT)
    r.raise_for_status()
    return r.content

def rsa_nums(pubkey) -> tuple[int,int] | None:
    if isinstance(pubkey, rsa.RSAPublicKey):
        pn = pubkey.public_numbers()
        return (pn.n, pn.e)
    return None

def live_tls_spki(host: str, port=443) -> str | None:
    ctx = ssl.create_default_context()
    try:
        with socket.create_connection((host, port), timeout=5) as sock:
            with ctx.wrap_socket(sock, server_hostname=host) as ssock:
                der = ssock.getpeercert(binary_form=True)
        cert = x509.load_der_x509_certificate(der)
        fp, pub = spki_sha256_from_cert(cert)
        return fp
    except Exception:
        return None

def main():
    entries = fetch_ct(BASE)
    seen = set()
    matches = []

    # facoltativo: stampa qualche nome dalle entries (aiuta a capire il terreno)
    for e in entries[:10]:
        raw = (e.get("name_value") or "").split("\n")
        dbg(f"[CT ENTRY] id={e.get('id') or e.get('min_cert_id')} names={raw}")

    for e in entries:
        cert_id = e.get("min_cert_id") or e.get("id")
        if cert_id is None:
            continue
        cert_id = int(cert_id)
        if cert_id in seen:
            continue
        seen.add(cert_id)

        try:
            blob = fetch_cert_blob(cert_id)
            certs = parse_any_cert(blob)
        except Exception as ex:
            dbg(f"[ERR] download/parse id={cert_id} -> {ex}")
            continue
        if not certs:
            continue

        for idx, cert in enumerate(certs, 1):
            names = extract_names(cert)
            fp, pub = spki_sha256_from_cert(cert)
            dbg(f"[TEST] id={cert_id} idx={idx}/{len(certs)} names={names or ['<no SAN/CN>']}")
            # skippa non-RSA se la target è RSA
            if target_nums and not isinstance(pub, rsa.RSAPublicKey):
                dbg("      -> non RSA, skip")
                continue

            if target_nums:
                pn = rsa_nums(pub)
                if pn:
                    same_n = pn[0] == target_nums[0]
                    same_e = pn[1] == target_nums[1]
                    dbg(f"[RSA ] bits={pub.key_size} e={pn[1]} n[:16hex]={hex(pn[0])[:18]}... eq_n={same_n} eq_e={same_e}")
                    if same_n and same_e:
                        print("[MATCH-RSA] crt.sh id", cert_id, "->", (names or ["<no SAN/CN>"]))
                        matches.append((cert_id, names))
                        break
            else:
                # target non-RSA: match su SPKI
                dbg(f"[SPKI] fp={fp} match={fp.lower()==TARGET_SPKI.lower()}")
                if fp.lower() == TARGET_SPKI.lower():
                    print("[MATCH-SPKI] crt.sh id", cert_id, "->", (names or ["<no SAN/CN>"]))
                    matches.append((cert_id, names))
                    break

        time.sleep(SLEEP)

    print("\n=== RISULTATO ===")
    if not matches:
        print("Nessun certificato (storico CT) usa esattamente quella chiave.")
    else:
        for cid, names in matches:
            print(f"- crt.sh id {cid}: {', '.join(names)}")

    # (OPZIONALE) verifica live lo stato attuale dei nomi incontrati
    # Attivalo se vuoi confermare cosa usa OGGI un host specifico
    # for _, names in matches:
    #     for h in names:
    #         cur = live_tls_spki(h)
    #         print("[LIVE]", h, "->", cur, "== target?", cur == TARGET_SPKI)

if __name__ == "__main__":
    main()
