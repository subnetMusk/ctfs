import requests

target = "https://127.0.0.1:9001/flag"

sess = requests.Session()

response = sess.get(target)

print(response.text)