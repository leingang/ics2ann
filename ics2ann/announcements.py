import csv, datetime
from typing import Generator, NamedTuple, IO

from .events import Event
from .dateutils import previous_monday


class Announcement(NamedTuple):
    """an announcement"""

    start: datetime.date
    end: datetime.date
    text: str


def announcements_from_events(es: list[Event]) -> Generator[Announcement, None, None]:
    """Generate announcements from a list of events"""
    my_date_format = "%A %B %-d"
    my_datetime_format = "%A %B %-d %-I:%M %p"
    for e in es:
        start_datetime = e.start.astimezone()
        end_date = e.start.astimezone().date()
        if e.is_availability or e.is_lesson or e.is_office_hour:
            pass
        elif e.is_duedate:
            if e.concerns_prequiz or e.concerns_postquiz:
                announcement_start = start_datetime - datetime.timedelta(days=7)
            else:
                announcement_start = previous_monday(start_datetime)
            a = Announcement(
                start=announcement_start,
                end=end_date,
                text="{} due {}".format(
                    e.subject, e.end.astimezone().strftime(my_datetime_format)
                ),
            )
            yield a
        elif e.is_exam:
            a = Announcement(
                start=previous_monday(start_datetime, 2),
                end=end_date,
                text="{} {}".format(
                    e.summary, e.start.astimezone().strftime(my_date_format)
                ),
            )
            yield a
        else:  # generic
            a = Announcement(
                start=previous_monday(start_datetime, 2),
                end=end_date,
                text="{}: {}".format(end_date.strftime(my_date_format), e.summary),
            )
            yield a


class CsvWriter(csv.DictWriter):
    """CSV Writer for a sequence of announcements"""

    _headers = ["startDate", "endDate", "announcementText"]

    _header_is_written = False

    def __init__(self, f: IO) -> None:
        super().__init__(f, fieldnames=self._headers)

    def write(self, a:Announcement) -> None:
        if not self._header_is_written:
            self.writeheader()
            self._header_is_written = True
        self.writerow({
            'startDate': a.start.strftime("%Y-%m-%d"),
            'endDate': a.end.strftime("%Y-%m-%d"),
            'announcementText': a.text
        })

    
