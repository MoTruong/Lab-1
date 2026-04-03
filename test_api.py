
import requests

LOCAL_URL  = "http://127.0.0.1:8000"

API_URL = LOCAL_URL

RESET = "\033[0m"; GREEN = "\033[92m"; RED = "\033[91m"; CYAN = "\033[96m"


def call_translate(message: str):
    response = requests.post(f"{API_URL}/generate", params={"message": message})
    print(f"  Input      : {message}")
    print(f"  Status     : {response.status_code}")
    data = response.json()
    if response.status_code == 200:
        print(f"  Translated : {data.get('translated')}")
    else:
        print(f"  Error      : {data}")
    return response


print(f"\n{CYAN}=== GET / ==={RESET}")
r = requests.get(f"{API_URL}/")
print(r.json())

print(f"\n{CYAN}=== GET /health ==={RESET}")
r = requests.get(f"{API_URL}/health")
print(r.json())

print(f"\n{CYAN}=== POST /generate — case 1 ==={RESET}")
call_translate("Hello, how are you?")

print(f"\n{CYAN}=== POST /generate — case 2 ==={RESET}")
call_translate("Artificial intelligence is transforming the world.")

print(f"\n{CYAN}=== POST /generate — case 3 ==={RESET}")
call_translate("Vietnam is a beautiful country with rich culture, stunning landscapes, and delicious food.")

print(f"\n{CYAN}=== POST /generate — case 4 ==={RESET}")
call_translate("Machine learning models require large amounts of data to achieve high accuracy.")

print(f"\n{CYAN}=== POST /generate — empty (lỗi dự kiến 422) ==={RESET}")
r = requests.post(f"{API_URL}/generate", params={"message": ""})
print(f"  Status : {r.status_code}")
print(f"  Result : {r.json()}\n")

print(f"\n{CYAN}=== GET /translate — thiếu param (lỗi dự kiến 422) ==={RESET}")
r = requests.get(f"{API_URL}/translate")
print(f"  Status : {r.status_code}")
print(f"  Result : {r.json()}\n")
