"""
Database helper functions for JSON file operations
"""
import json
import os
from typing import Dict, Any

def load_data(filepath: str) -> Dict[str, Any]:
    """
    Load data from JSON file. Returns empty dict if file doesn't exist.
    
    Args:
        filepath: Path to the JSON file
        
    Returns:
        Dictionary containing the loaded data
    """
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as file:
                return json.load(file)
        else:
            return {}
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading data from {filepath}: {e}")
        return {}

def save_data(data: Dict[str, Any], filepath: str) -> bool:
    """
    Save data to JSON file. Creates directory if it doesn't exist.
    
    Args:
        data: Dictionary to save
        filepath: Path to the JSON file
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
        return True
    except (IOError, OSError) as e:
        print(f"Error saving data to {filepath}: {e}")
        return False