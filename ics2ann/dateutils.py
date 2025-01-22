from datetime import datetime, date, timedelta


def previous_monday(dt: datetime, weeks: int = 1) -> date:
    """The Monday of the week *weeks* prior to *dt*.

    See https://stackoverflow.com/a/19686958/297797
    """
    return (dt - timedelta(dt.weekday(), weeks=weeks)).date()


def end_of_year(dt: datetime) -> date:
    """The last day of the year of *dt*"""
    return date(dt.year, 12, 31)

from datetime import datetime

class DifferentDaysError(Exception):
    """Custom exception raised when the datetime objects are on different days."""
    pass

def format_time_interval(start: datetime, end: datetime) -> str:
    """
    Format the time interval between two datetime objects into a specific string format.

    The format should follow the pattern: "Day, Month Day: start_time-end_time period",
    where the period (a.m. or p.m.) is applied after the end time. If the start time is
    before noon and the end time is after noon, the first time is labeled "a.m." and the 
    second time is labeled "p.m."

    Raises:
        DifferentDaysError: If the start and end datetimes belong to different days.

    Args:
        start (datetime): The start datetime
        end (datetime): The end datetime

    Returns:
        str: A formatted string representing the time interval.

    Examples:
        >>> start = datetime(2025, 1, 21, 10, 0)
        >>> end = datetime(2025, 1, 21, 15, 0)
        >>> format_time_interval(start, end)
        'Tuesday, January 21: 10:00 a.m.-3:00 p.m.'

        >>> start = datetime(2025, 1, 21, 14, 0)
        >>> end = datetime(2025, 1, 21, 16, 30)
        >>> format_time_interval(start, end)
        'Tuesday, January 21: 2:00-4:30 p.m.'

        >>> start = datetime(2025, 1, 21, 9, 30)
        >>> end = datetime(2025, 1, 21, 11, 0)
        >>> format_time_interval(start, end)
        'Tuesday, January 21: 9:30-11:00 a.m.'

        >>> start = datetime(2025, 1, 21, 23, 30)
        >>> end = datetime(2025, 1, 22, 1, 30)
        >>> format_time_interval(start, end) # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ...
        DifferentDaysError: Start and end times must be on the same day.
    """
    # Check if the start and end dates are on different days
    if start.date() != end.date():
        raise DifferentDaysError("Start and end times must be on the same day.")
    
    # Day of the week and date formatting
    date_format = start.strftime("%A, %B %-d")
    
    # Time formatting
    start_time = start.strftime("%-I:%M")
    end_time = end.strftime("%-I:%M")
    
    # Determine if times cross noon
    start_am_pm = "a.m." if start.hour < 12 else "p.m."
    end_am_pm = "a.m." if end.hour < 12 else "p.m."

    # Build the formatted time range
    if start_am_pm == end_am_pm:
        time_range = f"{start_time}-{end_time} {start_am_pm}"
    else:
        time_range = f"{start_time} {start_am_pm}-{end_time} {end_am_pm}"
    
    # Assemble the final output
    return f"{date_format}: {time_range}".strip()

# To run doctests in Python, you can execute:
if __name__ == "__main__":
    import doctest
    doctest.testmod()
