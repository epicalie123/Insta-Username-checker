# 🎰 Telegram Casino Bot

A modular Telegram casino bot built with Python and pyTelegramBotAPI. Features USD currency, daily bonuses, and an extensible game system.

## 🚀 Features

- **USD Currency**: All balances and transactions in USD format ($XX.XX)
- **Modular Games**: Easy to add new games without editing main.py
- **User Registration**: Automatic registration with $100 starting balance
- **Daily Bonus**: Claim $10 daily bonus once per day
- **JSON Database**: Simple file-based storage
- **Admin Panel**: Basic admin tools for management

## 📁 File Structure

```
casino_bot/
├── main.py               # Main bot file
├── config.py             # Configuration and constants
├── users.py              # User management system
├── admin.py              # Admin commands
├── database.py           # JSON file I/O helpers
├── games/
│   ├── __init__.py       # Auto-loads all games
│   └── dice.py           # Dice game example
├── utils/
│   └── common.py         # Utility functions
├── data/
│   └── users.json        # User data storage
├── requirements.txt       # Python dependencies
└── README.md            # This file
```

## 🛠 Setup Instructions

### 1. Get Bot Token
1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Create a new bot with `/newbot`
3. Copy the bot token

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Bot
Edit `config.py` and replace `YOUR_BOT_TOKEN_HERE` with your actual bot token:
```python
BOT_TOKEN = "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"
```

### 4. Run the Bot
```bash
python main.py
```

## 🎮 Available Commands

### User Commands
- `/start` - Register and get welcome message
- `/balance` - Check your USD balance
- `/daily` - Claim $10 daily bonus
- `/help` - Show help message

### Games
- `/dice` - Roll dice (win $50 on 6, lose $10 otherwise)

### Admin Commands (Admin only)
- `/admin` - Admin panel
- `/stats` - Show bot statistics
- `/addmoney <user_id> <amount>` - Add money to user

## 🎯 Game System

### Adding New Games
1. Create a new `.py` file in the `games/` folder
2. Include a `register(bot)` function
3. The game will be auto-loaded on startup

Example game structure:
```python
def register(bot):
    @bot.message_handler(commands=['mygame'])
    def my_game(message):
        # Game logic here
        pass
```

### Current Games
- **Dice**: Roll 1-6, win $50 on 6, lose $10 otherwise

## 💰 Currency System

- All balances stored in USD format
- Starting balance: $100.00
- Daily bonus: $10.00
- Dice game: Win $50.00, lose $10.00

## 🔧 Configuration

Edit `config.py` to customize:
- Bot token
- Starting balance
- Daily bonus amount
- Game payouts
- File paths

## 📊 Data Storage

User data is stored in `data/users.json`:
```json
{
  "user_id": {
    "balance": 150.00,
    "username": "user123",
    "first_name": "John",
    "registered_at": "2024-01-01T12:00:00",
    "last_daily": "2024-01-01T12:00:00"
  }
}
```

## 🛡️ Admin Features

To use admin commands:
1. Edit `admin.py`
2. Replace `123456789` with your Telegram user ID
3. Use `/admin` to access admin panel

## 🚀 Running in Production

For production deployment:
1. Use a process manager (systemd, supervisor)
2. Set up logging
3. Use environment variables for sensitive data
4. Consider using a proper database for larger scale

## 🤝 Contributing

To add new games:
1. Create game file in `games/` folder
2. Include `register(bot)` function
3. Test thoroughly
4. Submit pull request

## 📝 License

This project is open source. Feel free to modify and distribute.

## 🆘 Support

If you encounter issues:
1. Check the console output for errors
2. Verify your bot token is correct
3. Ensure all dependencies are installed
4. Check file permissions for data directory