import random
from users import get_user_balance, update_balance
from config import DICE_WIN, DICE_LOSE
from utils.common import format_usd, get_user_mention

def register(bot):
    """Register dice game commands with the bot"""
    
    @bot.message_handler(commands=['dice'])
    def dice_game(message):
        """Play dice game - roll 1-6, win $50 on 6, lose $10 otherwise"""
        user_id = message.from_user.id
        
        # Check if user is registered
        balance = get_user_balance(user_id)
        if balance == 0.0:
            bot.reply_to(message, "Please use /start to register first!")
            return
        
        # Roll the dice (1-6)
        roll = random.randint(1, 6)
        
        # Determine win/loss
        if roll == 6:
            # Win $50
            update_balance(user_id, DICE_WIN)
            new_balance = get_user_balance(user_id)
            result_message = f"🎲 You rolled a {roll}!\n"
            result_message += f"🎉 WINNER! +{format_usd(DICE_WIN)}\n"
            result_message += f"💰 New balance: {format_usd(new_balance)}"
        else:
            # Lose $10
            update_balance(user_id, -DICE_LOSE)
            new_balance = get_user_balance(user_id)
            result_message = f"🎲 You rolled a {roll}!\n"
            result_message += f"😢 Better luck next time! -{format_usd(DICE_LOSE)}\n"
            result_message += f"💰 New balance: {format_usd(new_balance)}"
        
        bot.reply_to(message, result_message)