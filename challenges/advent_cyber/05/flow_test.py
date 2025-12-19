import requests
import json
import time

target = "https://kramazon.csd.lol"
create_order_url = f"{target}/create-order"
finalize_url = f"{target}/finalize"

s = requests.Session()

# Step 0: Get the main page to set cookies
print("[*] Fetching main page...")
s.get(target)
print("Cookies:", s.cookies.get_dict())

# Step 1: Create Order
print("[*] Creating order...")
try:
    r = s.post(create_order_url, json={})
    if r.status_code != 200:
        print(f"Error creating order: {r.status_code} {r.text}")
        exit()
    
    order_data = r.json()
    print("Order Data:", json.dumps(order_data, indent=2))
    
    order_id = order_data.get("order_id")
    callback_url = order_data.get("callback_url")
    
    if callback_url.startswith("/"):
        callback_url = target + callback_url

    # Step 2: Check status (simulate wait)
    print("[*] Checking status (waiting 3s)...")
    time.sleep(3)
    
    r = s.get(callback_url)
    status_data = r.json()
    print("Status Data:", json.dumps(status_data, indent=2))
    
    current_user = status_data.get("internal", {}).get("user")
    print(f"Current User ID: {current_user}")

except Exception as e:
    print(f"Error: {e}")
