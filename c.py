import requests
from bs4 import BeautifulSoup

def check_instagram_profile(username):
    url = f"https://www.instagram.com/{username}/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    try:
        response = requests.get(url, headers=headers, allow_redirects=True)

        # Step 1: Check if it redirects to homepage (usually means account doesn't exist)
        if response.url != url:
            return {"exists": False, "message": "Instagram redirected — likely user does not exist."}

        # Step 2: Check if meta tag is available (bio/follower info)
        soup = BeautifulSoup(response.text, "html.parser")
        meta = soup.find("meta", attrs={"name": "description"})

        # Step 3: Use content of page title or meta to detect error message
        page_title = soup.title.string if soup.title else ""

        if "not found" in page_title.lower() or "error" in page_title.lower():
            return {"exists": False, "message": "Instagram says page not found."}

        if meta:
            return {
                "exists": True,
                "username": username,
                "summary": meta["content"]
            }
        else:
            return {
                "exists": True,
                "username": username,
                "message": "Profile exists, but no description meta tag found."
            }

    except Exception as e:
        return {"exists": None, "message": f"Error: {str(e)}"}


# Test it
if __name__ == "__main__":
    usernames = ["instagram", "nurturethedevilxyz1", "zuck"]
    for user in usernames:
        result = check_instagram_profile(user)
        print(f"Checking @{user}: {result}")
