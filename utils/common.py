def format_usd(amount):
    """Format amount as USD with 2 decimal places"""
    return f"${amount:.2f}"

def is_valid_amount(amount):
    """Check if amount is a valid positive number"""
    try:
        amount = float(amount)
        return amount > 0
    except (ValueError, TypeError):
        return False

def get_user_mention(user):
    """Get user mention for messages"""
    if user.username:
        return f"@{user.username}"
    else:
        return f"{user.first_name}"