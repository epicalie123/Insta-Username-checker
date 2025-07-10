import json
import os
from config import USERS_FILE

def load_data():
    """Load user data from JSON file"""
    try:
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, 'r') as file:
                return json.load(file)
        else:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
            return {}
    except (json.JSONDecodeError, FileNotFoundError):
        return {}

def save_data(data):
    """Save user data to JSON file"""
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
        with open(USERS_FILE, 'w') as file:
            json.dump(data, file, indent=2)
        return True
    except Exception as e:
        print(f"Error saving data: {e}")
        return False