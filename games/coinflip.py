import random
from users import get_user_balance, update_balance
from utils.common import format_usd

def register(bot):
    """Register coinflip game commands with the bot"""
    
    @bot.message_handler(commands=['coinflip'])
    def coinflip_game(message):
        """Play coinflip game - 50/50 chance to win $20 or lose $10"""
        user_id = message.from_user.id
        
        # Check if user is registered
        balance = get_user_balance(user_id)
        if balance == 0.0:
            bot.reply_to(message, "Please use /start to register first!")
            return
        
        # Flip the coin (heads or tails)
        result = random.choice(["heads", "tails"])
        
        # 50/50 chance to win
        if random.choice([True, False]):
            # Win $20
            update_balance(user_id, 20.00)
            new_balance = get_user_balance(user_id)
            result_message = f"🪙 Coin landed on: {result.upper()}\n"
            result_message += f"🎉 WINNER! +{format_usd(20.00)}\n"
            result_message += f"💰 New balance: {format_usd(new_balance)}"
        else:
            # Lose $10
            update_balance(user_id, -10.00)
            new_balance = get_user_balance(user_id)
            result_message = f"🪙 Coin landed on: {result.upper()}\n"
            result_message += f"😢 Better luck next time! -{format_usd(10.00)}\n"
            result_message += f"💰 New balance: {format_usd(new_balance)}"
        
        bot.reply_to(message, result_message)