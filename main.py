import telebot
from config import BOT_TOKEN
from users import register_user, get_balance_message, claim_daily_bonus, get_next_daily_time
from games import load_all_games
from admin import register as register_admin
from utils.common import format_usd

# Initialize bot
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    """Register new user and show welcome message"""
    user = message.from_user
    user_id = user.id
    
    # Register user (returns True if new user, False if already registered)
    is_new_user = register_user(user_id, user.username, user.first_name)
    
    if is_new_user:
        welcome_message = f"🎰 Welcome to Casino Bot, {user.first_name}!\n\n"
        welcome_message += f"💰 Starting balance: {format_usd(100.00)}\n\n"
        welcome_message += "🎮 Available games:\n"
        welcome_message += "• /dice - Roll dice (win $50 on 6)\n\n"
        welcome_message += "📋 Commands:\n"
        welcome_message += "• /balance - Check your balance\n"
        welcome_message += "• /daily - Claim daily bonus ($10)\n"
        welcome_message += "• /start - Show this message"
    else:
        welcome_message = f"🎰 Welcome back, {user.first_name}!\n\n"
        welcome_message += "🎮 Available games:\n"
        welcome_message += "• /dice - Roll dice (win $50 on 6)\n\n"
        welcome_message += "📋 Commands:\n"
        welcome_message += "• /balance - Check your balance\n"
        welcome_message += "• /daily - Claim daily bonus ($10)\n"
        welcome_message += "• /start - Show this message"
    
    bot.reply_to(message, welcome_message)

@bot.message_handler(commands=['balance'])
def balance(message):
    """Show user's current balance"""
    user_id = message.from_user.id
    balance_msg = get_balance_message(user_id)
    bot.reply_to(message, balance_msg)

@bot.message_handler(commands=['daily'])
def daily(message):
    """Claim daily bonus"""
    user_id = message.from_user.id
    
    success, msg = claim_daily_bonus(user_id)
    
    if success:
        # Get updated balance
        from users import get_user_balance
        new_balance = get_user_balance(user_id)
        msg += f"\n💰 New balance: {format_usd(new_balance)}"
    else:
        # Show when next daily is available
        next_daily = get_next_daily_time(user_id)
        if next_daily:
            from datetime import datetime
            now = datetime.now()
            time_left = next_daily - now
            hours = int(time_left.total_seconds() // 3600)
            minutes = int((time_left.total_seconds() % 3600) // 60)
            msg += f"\n⏰ Next daily available in: {hours}h {minutes}m"
    
    bot.reply_to(message, msg)

@bot.message_handler(commands=['help'])
def help_command(message):
    """Show help message"""
    help_text = "🎰 Casino Bot Help\n\n"
    help_text += "🎮 Games:\n"
    help_text += "• /dice - Roll a dice (1-6)\n"
    help_text += "  - Win $50.00 if you roll a 6\n"
    help_text += "  - Lose $10.00 otherwise\n\n"
    help_text += "💰 Commands:\n"
    help_text += "• /balance - Check your USD balance\n"
    help_text += "• /daily - Claim $10.00 daily bonus\n"
    help_text += "• /start - Register/Show welcome\n"
    help_text += "• /help - Show this help\n\n"
    help_text += "💡 Tip: Use /daily every day to earn free money!"
    
    bot.reply_to(message, help_text)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    """Handle any other messages"""
    bot.reply_to(message, "🤖 Use /help to see available commands!")

def main():
    """Main function to start the bot"""
    print("🎰 Starting Casino Bot...")
    
    # Load all games automatically
    print("🎮 Loading games...")
    loaded_games = load_all_games(bot)
    
    # Register admin commands
    register_admin(bot)
    
    print(f"✅ Bot started successfully!")
    print(f"🎮 Loaded {len(loaded_games)} games: {', '.join(loaded_games)}")
    print("🤖 Bot is running... Press Ctrl+C to stop")
    
    # Start polling
    try:
        bot.polling(none_stop=True)
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()