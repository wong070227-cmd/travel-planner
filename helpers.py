"""Helper functions for date formatting and calculations"""
from datetime import datetime, timedelta

def generate_date_display(date_str):
    """Convert YYYY-MM-DD to readable format"""
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.strftime("%B %d, %Y (%A)")
    except:
        return date_str

def get_dates_in_range(start_str, end_str):
    """Get all dates between start and end inclusive"""
    dates = []
    try:
        start = datetime.strptime(start_str, "%Y-%m-%d")
        end = datetime.strptime(end_str, "%Y-%m-%d")
        current = start
        while current <= end:
            dates.append(current.strftime("%Y-%m-%d"))
            current += timedelta(days=1)
    except:
        pass
    return dates