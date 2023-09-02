import csv
import datetime
import logging

import click
import icalevents.icalevents as icalevents

from .events import Event
from .dateutils import end_of_year
from .announcements import announcements_from_events, CsvWriter


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
    writer = CsvWriter(output)
    for a in announcements_from_events(events):
        writer.write(a)
