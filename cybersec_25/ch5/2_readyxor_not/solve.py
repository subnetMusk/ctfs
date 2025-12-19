import base64
from pwnlib.util.fiddling import xor

data = "El Psy Congroo"
enc_data = "IFhiPhZNYi0KWiUcCls="
enc_flag = "I3gDKVh1Lh4EVyMDBFo="

enc_data_c = base64.b64decode(enc_data)
enc_flag_c = base64.b64decode(enc_flag)

key = xor(data, enc_data_c)
flag = xor(key, enc_flag_c )

print(flag)

# Alpacaman