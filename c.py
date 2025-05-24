import requests

def is_instagram_username_available(username):
    url = f"https://www.instagram.com/{username}/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/",
        "Connection": "keep-alive",
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)

        # Check known error message in HTML
        if "Sorry, this page isn't available." in response.text:
            return True  # Username is available
        elif response.status_code == 200:
            return False  # Username is taken
        else:
            print(f"[!] Unexpected response code: {response.status_code}")
            return None
    except Exception as e:
        print(f"[!] Error checking username: {e}")
        return None

# --- Main Program ---
if __name__ == "__main__":
    username = input("Enter Instagram username to check: ").strip()
    result = is_instagram_username_available(username)

    if result is True:
        print(f"[+] Username '{username}' is AVAILABLE.")
    elif result is False:
        print(f"[-] Username '{username}' is TAKEN.")
    else:
        print(f"[!] Could not determine availability of '{username}'.")
