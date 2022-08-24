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


def is_duedate(e:Event) -> bool:
    if " - Due" in e.summary:
        (what,rest) = e.summary.split(' - ')
        e.what = what
        return True
    else:
        return False

def is_availability(e:Event) -> bool:
    """Test if an event is about something being available"""
    return " - Available" in e.summary

# def is_hw(event):
#     return (event['Type'] == 'Deadline' and re.search("(Homework|HW) [0|1-9]+ .*Due",event['Title']))

def is_exam(e:Event) -> bool:
    return "Exam" in e.summary

# def is_academic_calendar(event):
#     return event['Type'] == 'Academic Calendar'


class Announcement(NamedTuple):
    """a docstring"""
    start: datetime.date
    end: datetime.date
    text: str


def previous_monday(dt,weeks=1):
    """Return the datetime which is Monday of a week prior to the given datetime

    Args:
        dt: datetime to measure previous to
        weeks = 1: number of weeks previous

    See https://stackoverflow.com/a/19686958/297797
    """
    return dt - datetime.timedelta(dt.weekday(),weeks=weeks)


def announcements(es:list[Event]) -> Generator[Announcement, None, None]:
    """Generate announcements from a list of events"""
    my_date_format = "%A %B %-d"
    my_datetime_format = "%A %B %-d %-I:%M %p"
    for e in es:
        if is_availability(e):
            next
        if is_duedate(e):
            a = Announcement(
                    start = previous_monday(e.start.astimezone()).date(),
                    end = e.end.astimezone().date(),
                    text = "{} due {}".format(
                        e.what,
                        e.end.astimezone().strftime(my_datetime_format)))
            yield a
            next
        if is_exam(e):
            a = Announcement(
                    start = previous_monday(e.start.astimezone(),2).date(),
                    end = e.end.astimezone().date(),
                    text = "{} {}".format(
                        e.summary,
                        e.start.astimezone().strftime(my_date_format)))
            yield a
            next
        # # generic
        # a = Announcement(
        #     start = previous_monday(e.start.astimezone(),2).date(),
        #     end = e.end.astimezone().date(),
        #     text = e.summary)
        # yield a



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
    academic_calendar_url = "https://www.nyu.edu/feeds/events/ical/group/Academic-Calendar"
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
