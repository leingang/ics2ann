import csv, datetime
from typing import Generator, List, NamedTuple, IO
import re

from validators import url as is_url

from .events import Event
from .dateutils import previous_monday, format_time_interval
from .nyudatetime import rebrand_nyu_datetime


class Announcement(NamedTuple):
    """an announcement"""

    start: datetime.date
    end: datetime.date
    text: str


def officehours_from_events(es: List[Event]) -> Generator[Announcement, None, None]:
    """Generate office hour listings from a list of events"""
    for e in [ee for ee in es if ee.is_office_hour]:
        start_datetime = rebrand_nyu_datetime(e.start.astimezone())
        end_datetime = rebrand_nyu_datetime(e.end.astimezone())
        end_date = end_datetime.date()
        announcement_start = start_datetime - datetime.timedelta(days=7)
        match = re.search(r"CIWW \d+", e.location)
        if match:
            location = "in " + match.group()
        elif is_url(e.location):
            location = "online"
        else:
            location = "in " + e.location
        a = Announcement(
            start=announcement_start,
            end=end_date,
            text=format_time_interval(start_datetime, end_datetime) + " " + location,
        )
        yield a


def announcements_from_events(es: list[Event]) -> Generator[Announcement, None, None]:
    """Generate announcements from a list of events"""
    my_date_format = "%A %B %-d"
    my_datetime_format = "%A %B %-d %-I:%M %p"
    for e in es:
        start_datetime = rebrand_nyu_datetime(e.start.astimezone())
        end_datetime = rebrand_nyu_datetime(e.end.astimezone())
        end_date = end_datetime.date()
        if e.is_availability or e.is_office_hour:
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
        elif e.is_lesson:
            pass
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
    _write_headers = True

    def __init__(self, f: IO, headers: bool = True) -> None:
        super().__init__(f, fieldnames=self._headers)
        self._write_headers = headers

    def write(self, a: Announcement) -> None:
        if self._write_headers and not self._header_is_written:
            self.writeheader()
            self._header_is_written = True
        self.writerow(
            {
                "startDate": a.start.strftime("%Y-%m-%d"),
                "endDate": a.end.strftime("%Y-%m-%d"),
                "announcementText": a.text,
            }
        )


class TexWriter(object):
    """LaTeX writer for a sequence of announcements"""

    _header_is_written = False
    _write_headers = True

    def __init__(self, f: IO, headers: bool = True) -> None:
        self.f = f
        self._write_headers = headers

    def write(self, a: Announcement) -> None:
        f = self.f
        if self._write_headers and not self._header_is_written:
            f.write(r"\usepackage{datatool}" + "\n")
            f.write(r"\DTLnewdb{announcements}" + "\n")
            self._header_is_written = True
        f.write(r"\DTLnewrow{announcements}" + "\n")
        f.write(
            r"\DTLnewdbentry{announcements}{startDate}{"
            + a.start.strftime("%Y-%m-%d")
            + r"}"
            + "\n"
        )
        f.write(
            r"\DTLnewdbentry{announcements}{endDate}{"
            + a.end.strftime("%Y-%m-%d")
            + r"}"
            + "\n"
        )
        f.write(
            r"\DTLnewdbentry{announcements}{announcementText}{" + a.text + r"}" + "\n"
        )
