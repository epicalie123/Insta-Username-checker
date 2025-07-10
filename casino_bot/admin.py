"""
Admin tools for the casino bot
"""
from users import get_user_data, update_user_balance
from utils.common import format_usd

# List of admin user IDs (replace with actual admin IDs)
ADMIN_IDS = []  # Add admin Telegram user IDs here

def is_admin(user_id: str) -> bool:
    """
    Check if user is an admin.
    
    Args:
        user_id: Telegram user ID as string
        
    Returns:
        True if user is admin, False otherwise
    """
    return user_id in ADMIN_IDS

def register_admin_commands(bot):
    """
    Register admin-related bot commands.
    
    Args:
        bot: Telebot instance
    """
    
    @bot.message_handler(commands=['admin'])
    def handle_admin(message):
        user_id = str(message.from_user.id)
        
        if not is_admin(user_id):
            bot.reply_to(message, "❌ You don't have admin privileges.")
            return
        
        bot.reply_to(message, 
            "🔧 Admin Panel\n\n"
            "Available commands:\n"
            "/setbalance <user_id> <amount> - Set user balance\n"
            "/getuser <user_id> - Get user info")
    
    @bot.message_handler(commands=['setbalance'])
    def handle_set_balance(message):
        user_id = str(message.from_user.id)
        
        if not is_admin(user_id):
            bot.reply_to(message, "❌ You don't have admin privileges.")
            return
        
        try:
            parts = message.text.split()
            if len(parts) != 3:
                bot.reply_to(message, "Usage: /setbalance <user_id> <amount>")
                return
            
            target_user_id = parts[1]
            new_balance = float(parts[2])
            
            if update_user_balance(target_user_id, new_balance):
                bot.reply_to(message, 
                    f"✅ Set balance for user {target_user_id} to {format_usd(new_balance)}")
            else:
                bot.reply_to(message, f"❌ User {target_user_id} not found.")
                
        except ValueError:
            bot.reply_to(message, "❌ Invalid amount. Use numeric value.")
        except Exception as e:
            bot.reply_to(message, f"❌ Error: {str(e)}")
    
    @bot.message_handler(commands=['getuser'])
    def handle_get_user(message):
        user_id = str(message.from_user.id)
        
        if not is_admin(user_id):
            bot.reply_to(message, "❌ You don't have admin privileges.")
            return
        
        try:
            parts = message.text.split()
            if len(parts) != 2:
                bot.reply_to(message, "Usage: /getuser <user_id>")
                return
            
            target_user_id = parts[1]
            user_data = get_user_data(target_user_id)
            
            if user_data:
                bot.reply_to(message, 
                    f"👤 User Info\n"
                    f"ID: {target_user_id}\n"
                    f"Username: {user_data.get('username', 'N/A')}\n"
                    f"Balance: {format_usd(user_data['balance'])}\n"
                    f"Registration: {user_data.get('registration_date', 'N/A')}")
            else:
                bot.reply_to(message, f"❌ User {target_user_id} not found.")
                
        except Exception as e:
            bot.reply_to(message, f"❌ Error: {str(e)}")