import requests
import random
from time import sleep
from user_agent import generate_user_agent

# Function to check if a username is available
def check_instagram_username(username):
    headers = {
        "User-Agent": generate_user_agent(),
        "X-IG-App-ID": "936619743392459",  # Instagram Web App ID
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://www.instagram.com/",
    }

    # Fake login attempt to check username
    fake_password = "#PWD_INSTAGRAM_BROWSER:0:0:fake_password"
    data = {
        "username": username,
        "enc_password": fake_password,
        "optIntoOneTap": "false",
    }

    try:
        response = requests.post(
            "https://www.instagram.com/api/v1/web/accounts/login/ajax/",
            headers=headers,
            data=data,
        ).json()

        if response.get("user", False) or "showAccountRecoveryModal" in str(response):
            return f"❌ [UNAVAILABLE] @{username} (Account exists)"
        else:
            return f"✅ [AVAILABLE] @{username} (Username is free)"
    except Exception as e:
        return f"⚠️ [ERROR] @{username} (API issue: {e})"

# Usernames to check
usernames = ["nurturethedevil", "nurturethedevilxbej"]

for username in usernames:
    result = check_instagram_username(username)
    print(result)
    sleep(2)  # Avoid rate-limiting
