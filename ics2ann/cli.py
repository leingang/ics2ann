import csv
import datetime
import logging
import re
import sys
from typing import Generator, NamedTuple

import click
from icalevents.icalevents import events
from icalendar.cal import Event


class MyEvent(Event):
    """Add tests to Event class"""
    _event: Event
    subject: str

    def __init__(self,e:Event):
        self._event = e

    @property
    def start(self) -> datetime.datetime:
        return self._event.start

    @property
    def end(self) -> datetime.datetime:
        return self._event.end

    @property
    def summary(self) -> str:
        return self._event.summary

    @property
    def is_duedate(self) -> bool:
        if " - Due" in self.summary:
            (what,rest) = self.summary.split(' - ')
            self.subject = what
            return True
        else:
            return False

    @property
    def is_availability(self) -> bool:
        """Test if an event is about something being available"""
        return (" - Available" in self.summary or " - Availability Ends" in self.summary)

    @property
    def is_exam(self) -> bool:
        return "Exam" in self.summary and not "Period" in self.summary   

    @property
    def is_lesson(self) -> bool:
        return re.match("^§",self.summary)

class Announcement(NamedTuple):
    """a docstring"""
    start: datetime.date
    end: datetime.date
    text: str


def previous_monday(dt: datetime.datetime,weeks:int=1) -> datetime.date:
    """The Monday of the week *weeks* prior to *dt*.

    See https://stackoverflow.com/a/19686958/297797
    """
    return (dt - datetime.timedelta(dt.weekday(),weeks=weeks)).date()


def announcements(es:list[MyEvent]) -> Generator[Announcement, None, None]:
    """Generate announcements from a list of events"""
    my_date_format = "%A %B %-d"
    my_datetime_format = "%A %B %-d %-I:%M %p"
    for e in es:
        start_datetime = e.start.astimezone()
        end_date = e.start.astimezone().date()
        if e.is_availability or e.is_lesson:
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


@click.group()
@click.version_option()
def cli():
    "Process an ICS feed to generate announcements CSV"


@cli.command(name="command")
@click.argument(
    "example"
)
@click.option(
    "-o",
    "--option",
    help="An example option",
)
def first_command(example, option):
    "Command description goes here"
    click.echo("Here is some output")


@cli.command(name="read")
@click.argument("input")
@click.option("--output","-o",type=click.File('w'),default="-",
    help="Write output to FILENAME (default: stdout)")
def read_ics(input, output):
    click.echo(f"{input=}")
    today = datetime.date.today()
    end_date = datetime.date(2022,12,30)
    es = events(input,start=today,end=end_date)
    es2 = [MyEvent(e) for e in es]
    writer = csv.DictWriter(output,['startDate','endDate','announcementText'])
    writer.writeheader()
    for a in announcements(es2):
        writer.writerow({
            'startDate': a.start.strftime("%Y-%m-%d"),
            'endDate': a.end.strftime("%Y-%m-%d"),
            'announcementText': a.text
        })
