import requests

def is_username_available(username):
    url = f"https://www.instagram.com/{username}/?__a=1&__d=dis"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "application/json",
        "X-Requested-With": "XMLHttpRequest"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 404:
        return True  # Username is available
    elif response.status_code == 200:
        try:
            data = response.json()
            if "graphql" in data and "user" in data["graphql"]:
                return False  # Username exists
        except:
            return True  # If no user data in JSON, username is likely available
    else:
        print(f"[!] Unexpected status: {response.status_code}")
        return False

# --- MAIN ---
if __name__ == "__main__":
    username = input("Enter Instagram username to check: ").strip()
    if is_username_available(username):
        print(f"[+] The username '{username}' is AVAILABLE.")
    else:
        print(f"[-] The username '{username}' is TAKEN.")
