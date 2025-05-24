import requests
import random
import string
import threading
from bs4 import BeautifulSoup
import time

TELEGRAM_BOT_TOKEN = "7895423038:AAEo9FCKQwQaR_8GN3XR_Xe-yJ8_DacCBrk"
TELEGRAM_CHAT_ID = "7358850946"

# CONFIGURATION
USERNAME_LENGTH = 10
THREAD_COUNT = 10
NEEDED_AVAILABLE = 2

available_usernames = []
lock = threading.Lock()

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print(f"Telegram error: {e}")

def generate_username():
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(USERNAME_LENGTH))

def is_username_available(username):
    url = f"https://www.instagram.com/{username}/"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        meta = soup.find("meta", attrs={"name": "description"})

        if not meta:
            return True  # No meta tag = available
        return False

    except Exception:
        return False  # On error, assume not available

def check_loop():
    global available_usernames
    while True:
        with lock:
            if len(available_usernames) >= NEEDED_AVAILABLE:
                break

        username = generate_username()
        if is_username_available(username):
            with lock:
                if username not in available_usernames:
                    available_usernames.append(username)
                    print(f"[AVAILABLE] {username}")
                    send_telegram_message(f"Instagram username available: @{username}")
        else:
            print(f"[TAKEN] {username}")
        time.sleep(random.uniform(0.5, 1.2))  # Random delay to reduce risk

def main():
    threads = []

    for _ in range(THREAD_COUNT):
        t = threading.Thread(target=check_loop)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print("Done. Available usernames:", available_usernames)

if __name__ == "__main__":
    main()
