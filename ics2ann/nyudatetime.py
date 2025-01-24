from datetime import datetime


class NyuDateTime(datetime):
    """
    A subclass of datetime that overrides strftime to format the period "%p"
    as "a.m." or "p.m." instead of the default locale-specific AM/PM.

    Examples:
    >>> dt = NyuDateTime(2025, 1, 22, 10, 30)
    >>> dt.strftime("%A, %B %d, %I:%M %p")
    'Wednesday, January 22, 10:30 a.m.'

    >>> dt2 = NyuDateTime(2025, 1, 22, 15, 0)
    >>> dt2.strftime("%A, %B %d, %I:%M %p")
    'Wednesday, January 22, 03:00 p.m.'

    >>> dt3 = NyuDateTime(2025, 1, 22, 0, 15)
    >>> dt3.strftime("%A, %B %d, %I:%M %p")
    'Wednesday, January 22, 12:15 a.m.'
    """

    def strftime(self, format_str):
        """
        Overrides the strftime method of datetime objects.
        Formats the period ("%p") as "a.m." or "p.m.".
        """
        # Handle the custom period formatting
        if "%p" in format_str:
            # Replace "%p" with either "a.m." or "p.m." based on the time
            period = "a.m." if self.hour < 12 else "p.m."
            format_str = format_str.replace("%p", period)

        # Call the original strftime method (of the superclass) for other formatting
        return super().strftime(format_str)


def rebrand_nyu_datetime(dt: datetime) -> NyuDateTime:
    """
    Promotes a datetime object to an object of class NyuDateTime.

    Parameters:
    dt (datetime): A datetime object to promote.

    Returns:
    NyuDateTime: An instance of NyuDateTime with the same attributes as the original datetime object.

    Example:
    >>> dt = datetime(2025, 1, 22, 10, 30)
    >>> nyu_dt = rebrand_nyu_datetime(dt)
    >>> isinstance(nyu_dt, NyuDateTime)
    True
    >>> nyu_dt.strftime("%A, %B %d, %I:%M %p")
    'Wednesday, January 22, 10:30 a.m.'
    """
    return NyuDateTime(
        dt.year,
        dt.month,
        dt.day,
        dt.hour,
        dt.minute,
        dt.second,
        dt.microsecond,
        dt.tzinfo,
    )


# Example usage for manual testing
if __name__ == "__main__":
    import doctest

    doctest.testmod()
