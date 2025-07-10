import os
import importlib
import glob

def load_all_games(bot):
    """Auto-load all game modules and register them with the bot"""
    games_dir = os.path.dirname(__file__)
    
    # Get all .py files in the games directory (excluding __init__.py)
    game_files = glob.glob(os.path.join(games_dir, "*.py"))
    game_files = [f for f in game_files if not f.endswith("__init__.py")]
    
    loaded_games = []
    
    for game_file in game_files:
        try:
            # Extract module name from file path
            module_name = os.path.basename(game_file)[:-3]  # Remove .py extension
            
            # Import the module
            module = importlib.import_module(f"games.{module_name}")
            
            # Check if module has register function
            if hasattr(module, 'register'):
                module.register(bot)
                loaded_games.append(module_name)
                print(f"✅ Loaded game: {module_name}")
            else:
                print(f"⚠️  Skipped {module_name}: No register() function found")
                
        except Exception as e:
            print(f"❌ Failed to load {os.path.basename(game_file)}: {e}")
    
    print(f"🎮 Total games loaded: {len(loaded_games)}")
    return loaded_games