# 🎰 Telegram Casino Bot

A modular Telegram casino bot built with Python using pyTelegramBotAPI. Users can play games, manage USD balances, and enjoy a casino experience right in Telegram.

## 📂 Project Structure

```
casino_bot/
├── main.py               # Main bot entry point
├── config.py             # Configuration and constants
├── users.py              # User management system
├── admin.py              # Admin tools
├── database.py           # JSON file I/O helpers
├── requirements.txt      # Python dependencies
├── games/
│   ├── __init__.py       # Auto-loads all games
│   └── dice.py           # Example dice game
├── utils/
│   └── common.py         # USD formatting helpers
└── data/
    └── users.json        # User data storage
```

## 🚀 Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get Bot Token

1. Message [@BotFather](https://t.me/BotFather) on Telegram
2. Create a new bot with `/newbot`
3. Follow the instructions and get your bot token
4. Copy the token

### 3. Configure the Bot

Edit `config.py` and replace `YOUR_BOT_TOKEN_HERE` with your actual bot token:

```python
BOT_TOKEN = "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"
```

### 4. Run the Bot

```bash
cd casino_bot
python main.py
```

## 🎮 Available Commands

### User Commands
- `/start` - Register and get $100.00 starting balance
- `/balance` - Check your current USD balance
- `/daily` - Claim $10.00 daily bonus (once per day)
- `/help` - Show available commands

### Games
- `/dice` - Play dice game (roll 6 = win $50.00, others = lose $10.00)
- `/dicehelp` - Show dice game rules

### Admin Commands (for configured admins)
- `/admin` - Show admin panel
- `/setbalance <user_id> <amount>` - Set user balance
- `/getuser <user_id>` - Get user information

## 🔧 Configuration Options

Edit `config.py` to customize:

```python
STARTING_BALANCE = 100.00  # Starting balance for new users
DAILY_BONUS = 10.00       # Daily bonus amount
DICE_WIN = 50.00          # Amount won on dice roll of 6
DICE_LOSE = 10.00         # Amount lost on other dice rolls
```

## 🎯 Adding New Games

To add a new game:

1. Create a new `.py` file in the `games/` directory
2. Implement a `register(bot)` function that adds command handlers
3. The game will be automatically loaded when the bot starts

Example game template:

```python
from users import get_user_data, update_user_balance
from utils.common import format_usd

def register(bot):
    @bot.message_handler(commands=['mygame'])
    def handle_my_game(message):
        user_id = str(message.from_user.id)
        user_data = get_user_data(user_id)
        
        if not user_data:
            bot.reply_to(message, "❌ You need to register first. Use /start command.")
            return
        
        # Game logic here
        # Update balance with update_user_balance(user_id, new_balance)
```

## 🔐 Admin Setup

To enable admin commands:

1. Get your Telegram user ID (use [@userinfobot](https://t.me/userinfobot))
2. Add your ID to `ADMIN_IDS` list in `admin.py`:

```python
ADMIN_IDS = ["123456789"]  # Replace with your user ID
```

## 💾 Data Storage

User data is stored in `data/users.json` with the following structure:

```json
{
  "user_id": {
    "username": "telegram_username",
    "balance": 100.00,
    "last_daily": "2024-01-01T12:00:00",
    "registration_date": "2024-01-01T12:00:00"
  }
}
```

## 🎲 Game Features

### Dice Game
- Roll a number 1-6
- Roll 6: Win $50.00
- Roll 1-5: Lose $10.00
- Requires minimum balance of $10.00 to play

## 🛡️ Error Handling

The bot includes comprehensive error handling:
- Validates user registration before game play
- Checks sufficient balance before allowing bets
- Gracefully handles file I/O errors
- Provides helpful error messages to users

## 📝 Features

- ✅ Modular game system - easily add new games
- ✅ USD currency formatting throughout
- ✅ JSON-based data storage (no database required)
- ✅ Daily bonus system with cooldown
- ✅ Admin tools for user management
- ✅ Comprehensive error handling
- ✅ Auto-loading of games from `games/` directory
- ✅ Clean, documented code structure

## 🚨 Important Notes

- Keep your bot token secure and never commit it to version control
- The bot uses JSON files for data storage - ensure proper file permissions
- Test games thoroughly before deploying to production
- Monitor bot usage and implement rate limiting if needed

## 📞 Support

For issues or questions:
1. Check the console output for error messages
2. Verify your bot token is correct
3. Ensure all dependencies are installed
4. Check file permissions for the `data/` directory

Enjoy your casino bot! 🎰