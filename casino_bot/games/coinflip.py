"""
Coinflip game for the casino bot
Guess heads or tails: correct guess = win $25, wrong guess = lose $15
"""
import random
from users import get_user_data, update_user_balance
from utils.common import format_win_message, format_lose_message, format_usd

# Game configuration
COINFLIP_WIN = 25.00
COINFLIP_LOSE = 15.00

def register(bot):
    """
    Register the coinflip game with the bot.
    
    Args:
        bot: Telebot instance
    """
    
    @bot.message_handler(commands=['coinflip'])
    def handle_coinflip(message):
        user_id = str(message.from_user.id)
        user_data = get_user_data(user_id)
        
        # Check if user is registered
        if not user_data:
            bot.reply_to(message, "❌ You need to register first. Use /start command.")
            return
        
        current_balance = user_data['balance']
        
        # Check if user has enough balance to play
        if current_balance < COINFLIP_LOSE:
            bot.reply_to(message, 
                f"❌ Insufficient balance!\n"
                f"You need at least {format_usd(COINFLIP_LOSE)} to play coinflip.\n"
                f"Current balance: {format_usd(current_balance)}\n"
                f"Use /daily to get a bonus!")
            return
        
        # Parse user's guess from the command
        try:
            parts = message.text.split()
            if len(parts) != 2:
                bot.reply_to(message, 
                    "🪙 Usage: /coinflip <heads|tails>\n"
                    f"Win {format_usd(COINFLIP_WIN)} if correct, lose {format_usd(COINFLIP_LOSE)} if wrong!")
                return
            
            user_guess = parts[1].lower()
            if user_guess not in ['heads', 'tails']:
                bot.reply_to(message, 
                    "🪙 Please choose 'heads' or 'tails'\n"
                    "Example: /coinflip heads")
                return
                
        except:
            bot.reply_to(message, 
                "🪙 Usage: /coinflip <heads|tails>\n"
                f"Win {format_usd(COINFLIP_WIN)} if correct, lose {format_usd(COINFLIP_LOSE)} if wrong!")
            return
        
        # Flip the coin
        coin_result = random.choice(['heads', 'tails'])
        
        # Determine win or loss
        if user_guess == coin_result:
            # Win!
            new_balance = current_balance + COINFLIP_WIN
            update_user_balance(user_id, new_balance)
            
            bot.reply_to(message, 
                f"🪙 Coin result: {coin_result.upper()}\n"
                f"Your guess: {user_guess.upper()}\n"
                f"{format_win_message(COINFLIP_WIN, new_balance)}")
        else:
            # Lose
            new_balance = current_balance - COINFLIP_LOSE
            update_user_balance(user_id, new_balance)
            
            bot.reply_to(message, 
                f"🪙 Coin result: {coin_result.upper()}\n"
                f"Your guess: {user_guess.upper()}\n"
                f"{format_lose_message(COINFLIP_LOSE, new_balance)}")
    
    # Register help for the coinflip command
    @bot.message_handler(commands=['coinfliphelp'])
    def handle_coinflip_help(message):
        bot.reply_to(message, 
            f"🪙 Coinflip Game Rules:\n\n"
            f"• Usage: /coinflip <heads|tails>\n"
            f"• Correct guess: Win {format_usd(COINFLIP_WIN)}\n"
            f"• Wrong guess: Lose {format_usd(COINFLIP_LOSE)}\n"
            f"• Minimum balance required: {format_usd(COINFLIP_LOSE)}\n\n"
            f"Example: /coinflip heads")