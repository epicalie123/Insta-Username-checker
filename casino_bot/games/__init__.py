"""
Auto-loader for casino games
"""
import os
import importlib
import sys

def load_games(bot):
    """
    Automatically load and register all games from the games directory.
    
    Args:
        bot: Telebot instance
    """
    games_dir = os.path.dirname(__file__)
    loaded_games = []
    
    # Get all Python files in the games directory (excluding __init__.py)
    for filename in os.listdir(games_dir):
        if filename.endswith('.py') and filename != '__init__.py':
            module_name = filename[:-3]  # Remove .py extension
            
            try:
                # Import the game module
                module_path = f"games.{module_name}"
                if module_path in sys.modules:
                    # Reload if already imported
                    importlib.reload(sys.modules[module_path])
                    module = sys.modules[module_path]
                else:
                    module = importlib.import_module(module_path)
                
                # Check if the module has a register function
                if hasattr(module, 'register') and callable(getattr(module, 'register')):
                    # Register the game with the bot
                    module.register(bot)
                    loaded_games.append(module_name)
                    print(f"✅ Loaded game: {module_name}")
                else:
                    print(f"⚠️  Skipping {module_name}: no register() function found")
                    
            except Exception as e:
                print(f"❌ Error loading game {module_name}: {e}")
    
    print(f"🎮 Total games loaded: {len(loaded_games)}")
    return loaded_games