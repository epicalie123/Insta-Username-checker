import time
from datetime import datetime, timedelta
from database import load_data, save_data
from config import STARTING_BALANCE, DAILY_BONUS
from utils.common import format_usd

def register_user(user_id, username=None, first_name=None):
    """Register a new user with starting balance"""
    data = load_data()
    
    if str(user_id) not in data:
        data[str(user_id)] = {
            "balance": STARTING_BALANCE,
            "username": username,
            "first_name": first_name,
            "registered_at": datetime.now().isoformat(),
            "last_daily": None
        }
        save_data(data)
        return True
    return False

def get_user_balance(user_id):
    """Get user's current balance"""
    data = load_data()
    user_data = data.get(str(user_id))
    if user_data:
        return user_data.get("balance", 0.0)
    return 0.0

def update_balance(user_id, amount):
    """Update user's balance (positive or negative amount)"""
    data = load_data()
    user_id_str = str(user_id)
    
    if user_id_str not in data:
        return False
    
    data[user_id_str]["balance"] += amount
    save_data(data)
    return True

def can_claim_daily(user_id):
    """Check if user can claim daily bonus"""
    data = load_data()
    user_data = data.get(str(user_id))
    
    if not user_data:
        return False
    
    last_daily = user_data.get("last_daily")
    if not last_daily:
        return True
    
    try:
        last_daily_time = datetime.fromisoformat(last_daily)
        now = datetime.now()
        return (now - last_daily_time).days >= 1
    except:
        return True

def claim_daily_bonus(user_id):
    """Claim daily bonus for user"""
    if not can_claim_daily(user_id):
        return False, "You've already claimed your daily bonus today!"
    
    data = load_data()
    user_id_str = str(user_id)
    
    if user_id_str not in data:
        return False, "User not registered!"
    
    data[user_id_str]["balance"] += DAILY_BONUS
    data[user_id_str]["last_daily"] = datetime.now().isoformat()
    save_data(data)
    
    return True, f"Daily bonus claimed! +{format_usd(DAILY_BONUS)}"

def get_balance_message(user_id):
    """Get formatted balance message"""
    balance = get_user_balance(user_id)
    return f"Your balance: {format_usd(balance)}"

def get_next_daily_time(user_id):
    """Get time until next daily bonus is available"""
    data = load_data()
    user_data = data.get(str(user_id))
    
    if not user_data or not user_data.get("last_daily"):
        return None
    
    try:
        last_daily_time = datetime.fromisoformat(user_data["last_daily"])
        next_daily_time = last_daily_time + timedelta(days=1)
        return next_daily_time
    except:
        return None