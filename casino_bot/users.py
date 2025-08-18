"""
User management system for the casino bot
"""
import datetime
from typing import Optional
from database import load_data, save_data
from config import STARTING_BALANCE, DAILY_BONUS, USERS_DATA_FILE
from utils.common import format_balance_message, format_usd

def get_user_data(user_id: str) -> Optional[dict]:
    """
    Get user data from the database.
    
    Args:
        user_id: Telegram user ID as string
        
    Returns:
        User data dictionary or None if not found
    """
    data = load_data(USERS_DATA_FILE)
    return data.get(user_id)

def register_user(user_id: str, username: str = None) -> bool:
    """
    Register a new user with starting balance.
    
    Args:
        user_id: Telegram user ID as string
        username: Telegram username (optional)
        
    Returns:
        True if user was registered, False if already exists
    """
    data = load_data(USERS_DATA_FILE)
    
    if user_id in data:
        return False  # User already exists
    
    # Create new user
    data[user_id] = {
        'username': username,
        'balance': STARTING_BALANCE,
        'last_daily': None,
        'registration_date': datetime.datetime.now().isoformat()
    }
    
    return save_data(data, USERS_DATA_FILE)

def get_user_balance(user_id: str) -> float:
    """
    Get user's current balance.
    
    Args:
        user_id: Telegram user ID as string
        
    Returns:
        User's balance or 0.0 if user not found
    """
    user_data = get_user_data(user_id)
    return user_data['balance'] if user_data else 0.0

def update_user_balance(user_id: str, new_balance: float) -> bool:
    """
    Update user's balance.
    
    Args:
        user_id: Telegram user ID as string
        new_balance: New balance amount
        
    Returns:
        True if successful, False otherwise
    """
    data = load_data(USERS_DATA_FILE)
    
    if user_id not in data:
        return False
    
    data[user_id]['balance'] = round(new_balance, 2)  # Round to 2 decimal places
    return save_data(data, USERS_DATA_FILE)

def can_claim_daily(user_id: str) -> bool:
    """
    Check if user can claim daily bonus.
    
    Args:
        user_id: Telegram user ID as string
        
    Returns:
        True if user can claim daily bonus
    """
    user_data = get_user_data(user_id)
    if not user_data:
        return False
    
    last_daily = user_data.get('last_daily')
    if not last_daily:
        return True
    
    # Check if 24 hours have passed
    last_daily_date = datetime.datetime.fromisoformat(last_daily)
    now = datetime.datetime.now()
    return (now - last_daily_date).total_seconds() >= 24 * 3600

def claim_daily_bonus(user_id: str) -> tuple[bool, float]:
    """
    Claim daily bonus for user.
    
    Args:
        user_id: Telegram user ID as string
        
    Returns:
        Tuple of (success, new_balance)
    """
    if not can_claim_daily(user_id):
        return False, get_user_balance(user_id)
    
    data = load_data(USERS_DATA_FILE)
    if user_id not in data:
        return False, 0.0
    
    # Add daily bonus
    current_balance = data[user_id]['balance']
    new_balance = current_balance + DAILY_BONUS
    data[user_id]['balance'] = round(new_balance, 2)
    data[user_id]['last_daily'] = datetime.datetime.now().isoformat()
    
    if save_data(data, USERS_DATA_FILE):
        return True, new_balance
    else:
        return False, current_balance

def register_user_commands(bot):
    """
    Register user-related bot commands.
    
    Args:
        bot: Telebot instance
    """
    
    @bot.message_handler(commands=['start'])
    def handle_start(message):
        user_id = str(message.from_user.id)
        username = message.from_user.username
        
        if register_user(user_id, username):
            bot.reply_to(message, 
                f"🎰 Welcome to the Casino Bot!\n"
                f"You've been registered with a starting balance of {format_usd(STARTING_BALANCE)}.\n\n"
                f"Commands:\n"
                f"/balance - Check your balance\n"
                f"/daily - Claim daily bonus\n"
                f"/dice - Play dice game")
        else:
            balance = get_user_balance(user_id)
            bot.reply_to(message, 
                f"🎰 Welcome back to the Casino Bot!\n"
                f"{format_balance_message(balance)}")
    
    @bot.message_handler(commands=['balance'])
    def handle_balance(message):
        user_id = str(message.from_user.id)
        user_data = get_user_data(user_id)
        
        if not user_data:
            bot.reply_to(message, "❌ You need to register first. Use /start command.")
            return
        
        balance = user_data['balance']
        bot.reply_to(message, format_balance_message(balance))
    
    @bot.message_handler(commands=['daily'])
    def handle_daily(message):
        user_id = str(message.from_user.id)
        user_data = get_user_data(user_id)
        
        if not user_data:
            bot.reply_to(message, "❌ You need to register first. Use /start command.")
            return
        
        success, new_balance = claim_daily_bonus(user_id)
        
        if success:
            bot.reply_to(message, 
                f"🎁 Daily bonus claimed!\n"
                f"You received {format_usd(DAILY_BONUS)}.\n"
                f"New balance: {format_usd(new_balance)}")
        else:
            bot.reply_to(message, 
                f"⏰ You've already claimed your daily bonus today.\n"
                f"Come back tomorrow for another {format_usd(DAILY_BONUS)}!")