"""
Configuration settings for the Telegram Casino Bot
"""

# Bot Token - Replace with your actual bot token from BotFather
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

# User Balance Settings
STARTING_BALANCE = 100.00  # Starting balance in USD
DAILY_BONUS = 10.00       # Daily bonus amount in USD

# Game Settings
DICE_WIN = 50.00          # Amount won on dice roll of 6
DICE_LOSE = 10.00         # Amount lost on dice roll other than 6

# File paths
USERS_DATA_FILE = "data/users.json"