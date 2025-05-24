import requests
from bs4 import BeautifulSoup

def check_instagram_profile(username):
    url = f"https://www.instagram.com/{username}/"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 404:
            return {"exists": False, "message": "Username not found."}

        if response.status_code == 429:
            return {"exists": None, "message": "Rate limited. Try using proxies or delay."}

        if response.status_code != 200:
            return {"exists": None, "message": f"Unexpected response: {response.status_code}"}

        # Parse HTML
        soup = BeautifulSoup(response.text, "html.parser")

        # Find <meta> tag with description
        description_tag = soup.find("meta", attrs={"name": "description"})

        if not description_tag:
            return {"exists": True, "message": "Profile found, but no meta info available."}

        content = description_tag["content"]

        # Extract basic info from content string
        # Example: "3,152 Followers, 321 Following, 123 Posts - See Instagram photos..."
        return {
            "exists": True,
            "username": username,
            "summary": content
        }

    except Exception as e:
        return {"exists": None, "message": f"Error: {str(e)}"}


# Example usage
if __name__ == "__main__":
    usernames = ["instagram", "thisuserdoesnotexist777"]
    for user in usernames:
        result = check_instagram_profile(user)
        print(f"Checking @{user}: {result}")
