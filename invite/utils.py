from datetime import date, timedelta


def get_cutoff_date(days):
    """Calculate the cutoff date or return None if no time period was set."""
    if days is None or not isinstance(days, int):
        return None
    else:
        if days > 0:
            return date.today() - timedelta(days=days)
        elif days == 0:
            return date.today() + timedelta(days=2)
        else:
            return None
