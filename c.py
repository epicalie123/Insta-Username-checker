import requests

def check_username(username):
    # Method 1: Profile visit
    profile_url = f"https://www.instagram.com/{username}/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }

    profile_response = requests.get(profile_url, headers=headers)
    profile_available = profile_response.status_code == 404

    # Method 2: Recovery endpoint (check if username can be used for password recovery)
    recovery_url = "https://www.instagram.com/accounts/account_recovery_send_ajax/"
    data = {
        'email_or_username': username
    }
    recovery_headers = {
        'User-Agent': 'Mozilla/5.0',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://www.instagram.com/accounts/password/reset/',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    session = requests.Session()
    recovery_response = session.post(recovery_url, headers=recovery_headers, data=data)
    try:
        recovery_json = recovery_response.json()
        recovery_available = not recovery_json.get('account_exists', True)
    except:
        recovery_available = False

    # Combine logic
    if profile_available and recovery_available:
        print(f"[+] The username '{username}' is AVAILABLE.")
    else:
        print(f"[-] The username '{username}' is TAKEN.")

# --- MAIN ---
if __name__ == "__main__":
    user = input("Enter Instagram username to check: ").strip()
    check_username(user)
