from users import get_user_balance, update_balance
from database import load_data
from utils.common import format_usd

def register(bot):
    """Register admin commands with the bot"""
    
    @bot.message_handler(commands=['admin'])
    def admin_panel(message):
        """Admin panel - basic stub for future admin features"""
        user_id = message.from_user.id
        
        # Simple admin check (you can enhance this)
        if user_id == 123456789:  # Replace with your admin user ID
            admin_message = "🔧 Admin Panel\n\n"
            admin_message += "/stats - Show bot statistics\n"
            admin_message += "/addmoney <user_id> <amount> - Add money to user\n"
            admin_message += "/setbalance <user_id> <amount> - Set user balance"
            bot.reply_to(message, admin_message)
        else:
            bot.reply_to(message, "❌ Access denied. Admin only.")
    
    @bot.message_handler(commands=['stats'])
    def show_stats(message):
        """Show bot statistics"""
        user_id = message.from_user.id
        
        if user_id == 123456789:  # Replace with your admin user ID
            data = load_data()
            total_users = len(data)
            total_balance = sum(user.get("balance", 0) for user in data.values())
            
            stats_message = "📊 Bot Statistics\n\n"
            stats_message += f"👥 Total users: {total_users}\n"
            stats_message += f"💰 Total balance: {format_usd(total_balance)}"
            
            bot.reply_to(message, stats_message)
        else:
            bot.reply_to(message, "❌ Access denied. Admin only.")
    
    @bot.message_handler(commands=['addmoney'])
    def add_money(message):
        """Add money to user (admin only)"""
        user_id = message.from_user.id
        
        if user_id != 123456789:  # Replace with your admin user ID
            bot.reply_to(message, "❌ Access denied. Admin only.")
            return
        
        try:
            parts = message.text.split()
            if len(parts) != 3:
                bot.reply_to(message, "Usage: /addmoney <user_id> <amount>")
                return
            
            target_user_id = int(parts[1])
            amount = float(parts[2])
            
            if update_balance(target_user_id, amount):
                new_balance = get_user_balance(target_user_id)
                bot.reply_to(message, f"✅ Added {format_usd(amount)} to user {target_user_id}\nNew balance: {format_usd(new_balance)}")
            else:
                bot.reply_to(message, "❌ User not found!")
                
        except (ValueError, IndexError):
            bot.reply_to(message, "❌ Invalid format. Use: /addmoney <user_id> <amount>")