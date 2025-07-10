"""
Main entry point for the Telegram Casino Bot
"""
import telebot
from config import BOT_TOKEN
from users import register_user_commands
from admin import register_admin_commands
from games import load_games

def main():
    """
    Initialize and start the casino bot
    """
    # Check if bot token is configured
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("❌ Please set your BOT_TOKEN in config.py")
        print("   Get your token from @BotFather on Telegram")
        return
    
    # Create bot instance
    try:
        bot = telebot.TeleBot(BOT_TOKEN)
        print("🤖 Bot instance created successfully")
    except Exception as e:
        print(f"❌ Failed to create bot instance: {e}")
        return
    
    # Register user commands
    try:
        register_user_commands(bot)
        print("✅ User commands registered")
    except Exception as e:
        print(f"❌ Failed to register user commands: {e}")
        return
    
    # Register admin commands
    try:
        register_admin_commands(bot)
        print("✅ Admin commands registered")
    except Exception as e:
        print(f"❌ Failed to register admin commands: {e}")
        return
    
    # Load and register games
    try:
        load_games(bot)
        print("✅ Games loaded successfully")
    except Exception as e:
        print(f"❌ Failed to load games: {e}")
        return
    
    # Register a general help command
    @bot.message_handler(commands=['help'])
    def handle_help(message):
        help_text = (
            "🎰 Casino Bot Commands:\n\n"
            "👤 User Commands:\n"
            "/start - Register and get starting balance\n"
            "/balance - Check your balance\n"
            "/daily - Claim daily bonus\n\n"
            "🎮 Games:\n"
            "/dice - Play dice game\n"
            "/dicehelp - Dice game rules\n"
            "/coinflip <heads|tails> - Play coinflip game\n"
            "/coinfliphelp - Coinflip game rules\n\n"
            "ℹ️ Need help? Use /help"
        )
        bot.reply_to(message, help_text)
    
    # Handle unknown commands
    @bot.message_handler(func=lambda message: True)
    def handle_unknown(message):
        if message.text.startswith('/'):
            bot.reply_to(message, 
                "❓ Unknown command. Use /help to see available commands.")
    
    # Start the bot
    print("🚀 Starting casino bot...")
    print("Press Ctrl+C to stop the bot")
    
    try:
        bot.infinity_polling(none_stop=True)
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user")
    except Exception as e:
        print(f"❌ Bot error: {e}")

if __name__ == "__main__":
    main()