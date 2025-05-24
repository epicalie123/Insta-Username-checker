import requests
from user_agent import generate_user_agent

def check_instagram_username(username):
    headers = {
        "User-Agent": generate_user_agent(),
        "X-IG-App-ID": "936619743392459",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://www.instagram.com/",
    }

    data = {
        "username": username,
        "enc_password": "#PWD_INSTAGRAM_BROWSER:0:0:fake_password",
        "optIntoOneTap": "false",
    }

    try:
        response = requests.post(
            "https://www.instagram.com/api/v1/web/accounts/login/ajax/",
            headers=headers,
            data=data,
        ).json()

        if response.get("user", False) or "showAccountRecoveryModal" in str(response):
            return f"❌ @{username} is TAKEN"
        elif response.get("message") == "The username you entered doesn't appear to belong to an account.":
            return f"✅ @{username} is AVAILABLE"
        else:
            return f"⚠️ Couldn't check @{username} (Response: {response})"
    except Exception as e:
        return f"⚠️ Error checking @{username}: {str(e)}"

def main():
    print("Instagram Username Availability Checker")
    print("--------------------------------------")
    
    while True:
        username = input("\nEnter username to check (or 'exit' to quit): ").strip()
        if username.lower() == 'exit':
            break
        
        if not username:
            print("Please enter a username!")
            continue
            
        result = check_instagram_username(username)
        print(result)

if __name__ == "__main__":
    main()