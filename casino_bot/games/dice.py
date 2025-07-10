"""
Dice game for the casino bot
Roll a die: 6 = win $50, anything else = lose $10
"""
import random
from users import get_user_data, update_user_balance
from config import DICE_WIN, DICE_LOSE
from utils.common import format_win_message, format_lose_message, format_usd

def register(bot):
    """
    Register the dice game with the bot.
    
    Args:
        bot: Telebot instance
    """
    
    @bot.message_handler(commands=['dice'])
    def handle_dice(message):
        user_id = str(message.from_user.id)
        user_data = get_user_data(user_id)
        
        # Check if user is registered
        if not user_data:
            bot.reply_to(message, "❌ You need to register first. Use /start command.")
            return
        
        current_balance = user_data['balance']
        
        # Check if user has enough balance to play
        if current_balance < DICE_LOSE:
            bot.reply_to(message, 
                f"❌ Insufficient balance!\n"
                f"You need at least {format_usd(DICE_LOSE)} to play dice.\n"
                f"Current balance: {format_usd(current_balance)}\n"
                f"Use /daily to get a bonus!")
            return
        
        # Roll the dice (1-6)
        roll = random.randint(1, 6)
        
        # Determine win or loss
        if roll == 6:
            # Win!
            new_balance = current_balance + DICE_WIN
            update_user_balance(user_id, new_balance)
            
            bot.reply_to(message, 
                f"🎲 You rolled: {roll}\n"
                f"{format_win_message(DICE_WIN, new_balance)}")
        else:
            # Lose
            new_balance = current_balance - DICE_LOSE
            update_user_balance(user_id, new_balance)
            
            bot.reply_to(message, 
                f"🎲 You rolled: {roll}\n"
                f"{format_lose_message(DICE_LOSE, new_balance)}")
    
    # Register help for the dice command
    @bot.message_handler(commands=['dicehelp'])
    def handle_dice_help(message):
        bot.reply_to(message, 
            f"🎲 Dice Game Rules:\n\n"
            f"• Roll a 6: Win {format_usd(DICE_WIN)}\n"
            f"• Roll 1-5: Lose {format_usd(DICE_LOSE)}\n"
            f"• Minimum balance required: {format_usd(DICE_LOSE)}\n\n"
            f"Use /dice to play!")