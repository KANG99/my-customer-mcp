from datetime import datetime


def get_time(timezone: str = "UTC") -> str:
    """Get the current time in a specified timezone."""
    return f"Current time ({timezone}): {datetime.now().strftime('%H:%M:%S')}"
