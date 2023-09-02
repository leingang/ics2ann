import csv
import datetime
import logging
import re
import sys
from typing import Generator, NamedTuple

import click
import icalevents.icalevents as icalevents

from ics2ann.events import Event
from ics2ann.dateutils import previous_monday, end_of_year


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


@cli.command(
    name="read",
    help="Read iCal events from INPUT and create Announcements")
@click.argument("input")
@click.option("--output","-o",
    type=click.File('w'),
    default="-",
    help="Write output to FILENAME (default: stdout)")
@click.option("--start",
    type=click.DateTime(),
    default=datetime.date.today().isoformat(),
    help="Find events after this date (default: today)")
@click.option("--end",
    type=click.DateTime(),
    default=end_of_year(datetime.date.today()).isoformat(),
    help="Find events before this date (default: end of current year)")
def read_ics(input, output, start, end):
    click.echo(f"{input=}")
    events = [Event(e) for e in icalevents.events(input,start=start,end=end)]
    writer = csv.DictWriter(output,['startDate','endDate','announcementText'])
    writer.writeheader()
    for a in announcements_from_events(events):
        writer.writerow({
            'startDate': a.start.strftime("%Y-%m-%d"),
            'endDate': a.end.strftime("%Y-%m-%d"),
            'announcementText': a.text
        })
