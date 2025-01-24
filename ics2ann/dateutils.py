from datetime import datetime, date, timedelta


def previous_monday(dt: datetime, weeks: int = 1) -> date:
    """The Monday of the week *weeks* prior to *dt*.

    See https://stackoverflow.com/a/19686958/297797
    """
    return (dt - timedelta(dt.weekday(), weeks=weeks)).date()


def end_of_year(dt: datetime) -> date:
    """The last day of the year of *dt*"""
    return date(dt.year, 12, 31)


class DifferentDaysError(Exception):
    """Custom exception raised when the datetime objects are on different days."""

    pass


def format_time_interval(
    start: datetime,
    end: datetime,
    date_format: str = "%A, %B %d",
    time_format: str = "%-I:%M %p",
    start_time_format: str = "%-I:%M",
) -> str:
    """
    Formats the time interval between two datetime objects into a string.

    The date and time formats can be customized using the `date_format`, `time_format`, and `start_time_format` keyword arguments.

    The output format is "{formatted_date}: {formatted_start_time}–{formatted_end_time}".
    If the start and end times share the same period (am/pm), the start time is formatted using `start_time_format`,
    and the period is only added to the end time.

    Parameters:
    start (datetime): The start time.
    end (datetime): The end time.
    date_format (str): The format for the date. Default is "Wednesday, January 22" format ("%A, %B %d").
    time_format (str): The format for the end time. Default is "2:00 pm" format ("%I:%M %p").
    start_time_format (str): The format for the start time if the start and end have the same period. Default is "%-I:%M".

    Returns:
    str: A string representing the formatted time interval.

    Raises:
    DifferentDaysError: If the two datetime objects are not on the same day.

    Examples:
    >>> start = datetime(2025, 1, 22, 14, 0)
    >>> end = datetime(2025, 1, 22, 15, 0)
    >>> format_time_interval(start, end)
    'Wednesday, January 22: 2:00–3:00 PM'

    >>> start = datetime(2025, 1, 22, 10, 30)
    >>> end = datetime(2025, 1, 22, 14, 0)
    >>> format_time_interval(start, end)
    'Wednesday, January 22: 10:30 AM–2:00 PM'

    >>> start = datetime(2025, 1, 22, 10, 0)
    >>> end = datetime(2025, 1, 23, 11, 0)  # Different days
    >>> format_time_interval(start, end) # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    DifferentDaysError: Start and end times must be on the same day.
    """
    # Check if the start and end dates are on different days
    if start.date() != end.date():
        raise DifferentDaysError("Start and end times must be on the same day.")

    # Format the date and times
    formatted_date = start.strftime(date_format)
    formatted_end_time = end.strftime(time_format).lstrip("0")  # remove leading zero

    # Determine if start and end times share the same period (am/pm)
    start_period = start.strftime("%p").lower()
    end_period = end.strftime("%p").lower()

    if start_period == end_period:
        # If they share the same period, use the start_time_format for start time
        formatted_start_time = start.strftime(start_time_format).lstrip("0")
    else:
        # Otherwise, use the time_format for both
        formatted_start_time = start.strftime(time_format).lstrip("0")

    return f"{formatted_date}: {formatted_start_time}–{formatted_end_time}"


if __name__ == "__main__":
    import doctest

    doctest.testmod()
