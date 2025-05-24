import requests

def is_username_available(username):
    url = f"https://www.instagram.com/{username}/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "DNT": "1",  # Do Not Track
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 404:
        return True  # Username is available
    elif response.status_code == 200:
        return False  # Username is taken
    else:
        print(f"[!] Unexpected response ({response.status_code}) for '{username}'")
        return False

# --- MAIN ---
if __name__ == "__main__":
    username = input("Enter Instagram username to check: ").strip()
    if is_username_available(username):
        print(f"[+] The username '{username}' is AVAILABLE.")
    else:
        print(f"[-] The username '{username}' is TAKEN.")
