import datetime


def previous_monday(dt: datetime.datetime, weeks: int = 1) -> datetime.date:
    """The Monday of the week *weeks* prior to *dt*.

    See https://stackoverflow.com/a/19686958/297797
    """
    return (dt - datetime.timedelta(dt.weekday(), weeks=weeks)).date()


def end_of_year(dt: datetime.datetime) -> datetime.date:
    """The last day of the year of *dt*"""
    return datetime.date(dt.year, 12, 31)
