"""
Common utility functions for the casino bot
"""

def format_usd(amount: float) -> str:
    """
    Format a float amount as USD currency string.
    
    Args:
        amount: The amount to format
        
    Returns:
        String formatted as $XX.XX
    """
    return f"${amount:.2f}"

def format_balance_message(balance: float) -> str:
    """
    Format a balance message for display to users.
    
    Args:
        balance: The user's balance
        
    Returns:
        Formatted balance message
    """
    return f"Your balance: {format_usd(balance)}"

def format_win_message(amount: float, new_balance: float) -> str:
    """
    Format a win message.
    
    Args:
        amount: Amount won
        new_balance: User's new balance
        
    Returns:
        Formatted win message
    """
    return f"🎉 You won {format_usd(amount)}!\nNew balance: {format_usd(new_balance)}"

def format_lose_message(amount: float, new_balance: float) -> str:
    """
    Format a lose message.
    
    Args:
        amount: Amount lost
        new_balance: User's new balance
        
    Returns:
        Formatted lose message
    """
    return f"😔 You lost {format_usd(amount)}.\nNew balance: {format_usd(new_balance)}"