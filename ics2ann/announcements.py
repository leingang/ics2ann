import datetime
from typing import Generator, NamedTuple

from .events import Event
from .dateutils import previous_monday


class Announcement(NamedTuple):
    """a docstring"""
    start: datetime.date
    end: datetime.date
    text: str


def announcements_from_events(es:list[Event]) -> Generator[Announcement, None, None]:
    """Generate announcements from a list of events"""
    my_date_format = "%A %B %-d"
    my_datetime_format = "%A %B %-d %-I:%M %p"
    for e in es:
        start_datetime = e.start.astimezone()
        end_date = e.start.astimezone().date()
        if e.is_availability or e.is_lesson or e.is_office_hour:
            pass
        elif e.is_duedate:
            a = Announcement(
                    start = previous_monday(start_datetime),
                    end = end_date,
                    text = "{} due {}".format(
                        e.subject,
                        e.end.astimezone().strftime(my_datetime_format)))
            yield a
        elif e.is_exam:
            a = Announcement(
                    start = previous_monday(start_datetime,2),
                    end = end_date,
                    text = "{} {}".format(
                        e.summary,
                        e.start.astimezone().strftime(my_date_format)))
            yield a
        else: # generic
            a = Announcement(
                start = previous_monday(start_datetime,2),
                end = end_date,
                text = "{}: {}".format(end_date.strftime(my_date_format),e.summary))
            yield a
