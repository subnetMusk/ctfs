import requests
from urllib.parse import unquote

target = "https://kramazon.csd.lol/"

try:
    se = requests.Session()
    req = se.get(target)

    print(f"--- Status Code: {req.status_code} ---")
    
    print("\n--- Cookies ---")
    for k, v in req.cookies.get_dict().items():
        print(f"{k}: {v}")

    print("\n--- Headers ---")
    for k, v in req.headers.items():
        print(f"{k}: {v}")

    print("\n--- HTML Content (truncated) ---")
    print(req.text[:2000])

    print("\n--- Searching for keywords ---")
    keywords = ["checkout", "priority", "shipping", "admin", "cart", "flag"]
    for kw in keywords:
        if kw in req.text.lower():
            print(f"Found '{kw}' in HTML")

    # Check robots.txt
    print("\n--- robots.txt ---")
    robots = se.get(target + "robots.txt")
    if robots.status_code == 200:
        print(robots.text)
    else:
        print("No robots.txt found")

except Exception as e:
    print(e)
